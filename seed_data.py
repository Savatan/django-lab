"""
seed_data.py — тестовые данные для портала заявок (Лаба №4).
Запуск:  python3 manage.py shell < seed_data.py

Создаёт трёх пользователей с разными ролями:
  user1    / pass12345  — обычный пользователь
  moder1   / pass12345  — модератор
  admin1   / pass12345  — администратор (суперпользователь)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
django.setup()

from django.contrib.auth.models import User
from tickets.models import (
    UserProfile, UserSettings, Ticket, Comment, TicketHistory,
)

# Очистка (кроме существующих суперпользователей)
Comment.objects.all().delete()
TicketHistory.objects.all().delete()
Ticket.objects.all().delete()
User.objects.filter(username__in=['user1', 'moder1', 'admin1']).delete()


def make_user(username, role, is_super=False):
    user = User.objects.create_user(username=username, password='pass12345')
    if is_super:
        user.is_staff = True
        user.is_superuser = True
        user.save()
    # Профиль и настройки уже созданы сигналом post_save — обновляем роль
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    UserSettings.objects.get_or_create(user=user)
    return user


u_user = make_user('user1', UserProfile.ROLE_USER)
u_mod = make_user('moder1', UserProfile.ROLE_MODERATOR)
u_admin = make_user('admin1', UserProfile.ROLE_ADMIN, is_super=True)
print('Создано пользователей: 3 (user1 / moder1 / admin1, пароль pass12345)')

# ── Заявки ───────────────────────────────────────────────────
t1 = Ticket.objects.create(
    title='Не работает VPN', description='Не подключается к корпоративному VPN из дома.',
    service='Сеть', owner=u_user, status=Ticket.STATUS_NEW, priority=Ticket.PRIORITY_HIGH)
t2 = Ticket.objects.create(
    title='Доступ к 1С', description='Нужен доступ к базе бухгалтерии.',
    service='1С', owner=u_user, status=Ticket.STATUS_IN_PROGRESS, priority=Ticket.PRIORITY_MEDIUM)
t3 = Ticket.objects.create(
    title='Замена картриджа', description='Закончился тонер в принтере на 3 этаже.',
    service='Оргтехника', owner=u_mod, status=Ticket.STATUS_RESOLVED, priority=Ticket.PRIORITY_LOW)

# ── Комментарии и история ────────────────────────────────────
Comment.objects.create(ticket=t1, author=u_mod, text='Принял в работу, проверяю настройки.')
Comment.objects.create(ticket=t2, author=u_user, text='Очень нужно, горящие сроки.')
TicketHistory.objects.create(ticket=t2, user=u_mod, field='Статус',
                             old_value='Новая', new_value='В работе')

print(f'Создано заявок: {Ticket.objects.count()}')
print(f'Создано комментариев: {Comment.objects.count()}')
print('\n✅ База заполнена!')
print('Запустите: python3 manage.py runserver')
print('Войдите:   http://127.0.0.1:8000/login/')
