from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Профиль пользователя с ролью."""

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile', verbose_name='Пользователь',
    )
    role = models.CharField(
        'Роль', max_length=20, choices=ROLE_CHOICES, default=ROLE_USER,
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_moderator(self):
        return self.role in (self.ROLE_MODERATOR, self.ROLE_ADMIN)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class UserSettings(models.Model):
    """Пользовательские настройки."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='settings', verbose_name='Пользователь',
    )
    email_notifications = models.BooleanField('Уведомления на email', default=True)
    items_per_page = models.PositiveSmallIntegerField('Заявок на странице', default=10)
    theme = models.CharField(
        'Тема', max_length=10,
        choices=[('light', 'Светлая'), ('dark', 'Тёмная')], default='light',
    )

    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'

    def __str__(self):
        return f'Настройки {self.user.username}'


class Ticket(models.Model):
    """Заявка на внутренний сервис."""

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_RESOLVED, 'Решена'),
        (STATUS_CLOSED, 'Закрыта'),
    ]

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Низкий'),
        (PRIORITY_MEDIUM, 'Средний'),
        (PRIORITY_HIGH, 'Высокий'),
    ]

    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    service = models.CharField('Сервис', max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='tickets', verbose_name='Владелец',
    )
    status = models.CharField(
        'Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW,
    )
    priority = models.CharField(
        'Приоритет', max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM,
    )
    attachment = models.FileField(
        'Вложение', upload_to='attachments/', blank=True, null=True,
    )
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} {self.title}'

    @property
    def is_closed(self):
        return self.status in (self.STATUS_RESOLVED, self.STATUS_CLOSED)


class Comment(models.Model):
    """Комментарий к заявке."""
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Заявка',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор',
    )
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий {self.author.username} к #{self.ticket_id}'


class TicketHistory(models.Model):
    """История изменений заявки."""
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE,
        related_name='history', verbose_name='Заявка',
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name='Кто изменил',
    )
    field = models.CharField('Поле', max_length=50)
    old_value = models.CharField('Старое значение', max_length=255, blank=True)
    new_value = models.CharField('Новое значение', max_length=255, blank=True)
    changed_at = models.DateTimeField('Когда', auto_now_add=True)

    class Meta:
        verbose_name = 'Изменение заявки'
        verbose_name_plural = 'История изменений'
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.field}: {self.old_value} -> {self.new_value}'


class AuditLog(models.Model):
    """Журнал аудита действий (заполняется middleware)."""
    request_id = models.CharField('Request ID', max_length=40, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Пользователь',
    )
    ip = models.GenericIPAddressField('IP-адрес', null=True, blank=True)
    user_agent = models.CharField('User-Agent', max_length=300, blank=True)
    method = models.CharField('HTTP-метод', max_length=10)
    path = models.CharField('Путь', max_length=300)
    status_code = models.PositiveSmallIntegerField('Код ответа', default=0)
    created_at = models.DateTimeField('Время', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись аудита'
        verbose_name_plural = 'Audit log'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.request_id}] {self.method} {self.path} -> {self.status_code}'


# ── Автосоздание профиля и настроек для новых пользователей ──────────────────
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def ensure_profile(sender, instance, created, **kwargs):
    if created:
        role = UserProfile.ROLE_ADMIN if instance.is_superuser else UserProfile.ROLE_USER
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})
        UserSettings.objects.get_or_create(user=instance)
