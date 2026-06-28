
from django.utils import timezone
from datetime import timedelta


def get_role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'admin'
    if hasattr(user, 'profile'):
        return user.profile.role
    return 'user'


def is_moderator(user):
    return get_role(user) in ('moderator', 'admin')


def is_admin(user):
    return get_role(user) == 'admin'


def can_view_ticket(user, ticket):
    """Видеть заявку может владелец или модератор/админ."""
    if not user.is_authenticated:
        return False
    return ticket.owner_id == user.id or is_moderator(user)


def can_edit_ticket(user, ticket):
    if not user.is_authenticated:
        return False
    if is_moderator(user):
        return True
    if ticket.owner_id != user.id:
        return False
    if ticket.is_closed:
        return False

    deadline = ticket.updated_at + timedelta(hours=24)
    return timezone.now() <= deadline


def can_change_status(user, ticket):
    """Менять статус могут только модераторы и админы."""
    return is_moderator(user)


def can_delete_ticket(user, ticket):
    """Удалять заявку может владелец (если новая) или админ."""
    if not user.is_authenticated:
        return False
    if is_admin(user):
        return True
    return ticket.owner_id == user.id and ticket.status == ticket.STATUS_NEW


def can_comment(user, ticket):
    """Комментировать может тот, кто видит заявку, если она не закрыта."""
    if not can_view_ticket(user, ticket):
        return False
    return not ticket.is_closed


def can_moderate(user):
    """Доступ к панели модератора."""
    return is_moderator(user)
