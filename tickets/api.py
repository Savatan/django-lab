"""
tickets/api.py
==============
Простой REST API на чистом Django (без сторонних зависимостей).
Эндпоинты для основных сущностей: заявки и комментарии.

  GET  /api/tickets/             — список заявок (с учётом роли)
  POST /api/tickets/             — создать заявку
  GET  /api/tickets/<id>/        — детали заявки
  GET  /api/tickets/<id>/comments/  — комментарии заявки
  POST /api/tickets/<id>/comments/  — добавить комментарий

Все ответы содержат заголовок X-Request-ID (его добавляет middleware).
Защищено rate-limit и working-hours middleware.
"""

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import Ticket, Comment
from . import permissions as perm


def _require_login(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)
    return None


def _ticket_to_dict(t):
    return {
        'id': t.id,
        'title': t.title,
        'service': t.service,
        'status': t.status,
        'status_display': t.get_status_display(),
        'priority': t.priority,
        'owner': t.owner.username,
        'created_at': t.created_at.isoformat(),
        'updated_at': t.updated_at.isoformat(),
        'comments_count': t.comments.count(),
    }


def _comment_to_dict(c):
    return {
        'id': c.id,
        'author': c.author.username,
        'text': c.text,
        'created_at': c.created_at.isoformat(),
    }


@csrf_exempt
def api_tickets(request):
    """GET — список, POST — создание."""
    auth = _require_login(request)
    if auth:
        return auth

    if request.method == 'GET':
        if perm.is_moderator(request.user):
            qs = Ticket.objects.select_related('owner').all()
        else:
            qs = Ticket.objects.select_related('owner').filter(owner=request.user)

        # фильтр по статусу
        status = request.GET.get('status')
        if status:
            qs = qs.filter(status=status)

        data = [_ticket_to_dict(t) for t in qs]
        return JsonResponse({'count': len(data), 'results': data})

    if request.method == 'POST':
        try:
            payload = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)

        title = payload.get('title')
        description = payload.get('description', '')
        service = payload.get('service', '')
        if not title:
            return JsonResponse({'error': 'Поле title обязательно'}, status=400)

        ticket = Ticket.objects.create(
            title=title, description=description, service=service,
            owner=request.user,
            priority=payload.get('priority', Ticket.PRIORITY_MEDIUM),
        )
        return JsonResponse(_ticket_to_dict(ticket), status=201)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


@csrf_exempt
def api_ticket_detail(request, pk):
    """GET — детали одной заявки."""
    auth = _require_login(request)
    if auth:
        return auth

    ticket = get_object_or_404(Ticket, pk=pk)
    if not perm.can_view_ticket(request.user, ticket):
        return JsonResponse({'error': 'Нет доступа'}, status=403)

    if request.method == 'GET':
        data = _ticket_to_dict(ticket)
        data['description'] = ticket.description
        return JsonResponse(data)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


@csrf_exempt
def api_ticket_comments(request, pk):
    """GET — комментарии, POST — добавить комментарий."""
    auth = _require_login(request)
    if auth:
        return auth

    ticket = get_object_or_404(Ticket, pk=pk)
    if not perm.can_view_ticket(request.user, ticket):
        return JsonResponse({'error': 'Нет доступа'}, status=403)

    if request.method == 'GET':
        data = [_comment_to_dict(c) for c in ticket.comments.select_related('author')]
        return JsonResponse({'count': len(data), 'results': data})

    if request.method == 'POST':
        if not perm.can_comment(request.user, ticket):
            return JsonResponse({'error': 'Нельзя комментировать'}, status=403)
        try:
            payload = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        text = payload.get('text')
        if not text:
            return JsonResponse({'error': 'Поле text обязательно'}, status=400)
        c = Comment.objects.create(ticket=ticket, author=request.user, text=text)
        return JsonResponse(_comment_to_dict(c), status=201)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
