
import time
import uuid
import logging
import threading

from django.core.cache import cache
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone

logger = logging.getLogger('portal')

_local = threading.local()


def get_current_user():
    return getattr(_local, 'user', None)


def get_current_request_id():
    return getattr(_local, 'request_id', '')


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

class RequestIDMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming = request.META.get('HTTP_X_REQUEST_ID')
        request_id = incoming or uuid.uuid4().hex[:12]
        request.request_id = request_id
        _local.request_id = request_id

        logger.info('start request_id=%s %s %s',
                    request_id, request.method, request.path)

        response = self.get_response(request)
        response['X-Request-ID'] = request_id
        return response

class CurrentUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.user = getattr(request, 'user', None)
        try:
            response = self.get_response(request)
        finally:

            _local.user = None
        return response

class RateLimitMiddleware:
  
    LIMIT = 30    
    WINDOW = 60     
    PROTECTED_PREFIX = '/api/'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(self.PROTECTED_PREFIX):
            ip = _client_ip(request) or 'unknown'
            key = f'ratelimit:{ip}:{request.path}'
            count = cache.get(key, 0)

            if count >= self.LIMIT:
                logger.warning('rate limit exceeded request_id=%s ip=%s path=%s',
                               get_current_request_id(), ip, request.path)
                return JsonResponse(
                    {'error': 'Превышен лимit запросов. Попробуйте позже.',
                     'request_id': get_current_request_id()},
                    status=429,
                )
            # увеличиваем счётчик (с истечением окна)
            cache.set(key, count + 1, timeout=self.WINDOW)

        return self.get_response(request)

class WorkingHoursMiddleware:

    WORK_START = 9
    WORK_END = 18
    DANGEROUS_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}
    PROTECTED_PREFIXES = ('/tickets/', '/api/', '/moderator/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in self.DANGEROUS_METHODS and \
                request.path.startswith(self.PROTECTED_PREFIXES):

            user = getattr(request, 'user', None)
            is_admin = bool(
                user and user.is_authenticated and
                (user.is_superuser or
                 (hasattr(user, 'profile') and user.profile.is_admin))
            )

            if not is_admin:
                hour = timezone.localtime().hour
                if not (self.WORK_START <= hour < self.WORK_END):
                    logger.warning(
                        'blocked off-hours op request_id=%s user=%s path=%s hour=%s',
                        get_current_request_id(),
                        getattr(user, 'username', 'anon'),
                        request.path, hour,
                    )
                    msg = (f'Опасные операции доступны только с '
                           f'{self.WORK_START}:00 до {self.WORK_END}:00. '
                           f'Сейчас {hour}:00.')
                    if request.path.startswith('/api/'):
                        return JsonResponse({'error': msg}, status=403)
                    return HttpResponseForbidden(msg)

        return self.get_response(request)


class AuditMiddleware:

    SKIP_PREFIXES = ('/static/', '/media/', '/favicon.ico')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = int((time.monotonic() - start) * 1000)

        if request.path.startswith(self.SKIP_PREFIXES):
            return response

        from .models import AuditLog

        user = getattr(request, 'user', None)
        if user is not None and not user.is_authenticated:
            user = None

        try:
            AuditLog.objects.create(
                request_id=getattr(request, 'request_id', ''),
                user=user,
                ip=_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:300],
                method=request.method,
                path=request.path[:300],
                status_code=response.status_code,
            )
        except Exception as exc:  
            logger.error('audit write failed: %s', exc)

        logger.info('end request_id=%s status=%s %dms',
                    getattr(request, 'request_id', ''),
                    response.status_code, duration_ms)
        return response
