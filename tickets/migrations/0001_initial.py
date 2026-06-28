"""Миграция 0001 — все модели портала заявок."""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('service', models.CharField(max_length=100, verbose_name='Сервис')),
                ('status', models.CharField(
                    choices=[('new', 'Новая'), ('in_progress', 'В работе'),
                             ('resolved', 'Решена'), ('closed', 'Закрыта')],
                    default='new', max_length=20, verbose_name='Статус')),
                ('priority', models.CharField(
                    choices=[('low', 'Низкий'), ('medium', 'Средний'),
                             ('high', 'Высокий')],
                    default='medium', max_length=10, verbose_name='Приоритет')),
                ('attachment', models.FileField(blank=True, null=True,
                                                upload_to='attachments/',
                                                verbose_name='Вложение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлена')),
                ('owner', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tickets', to=settings.AUTH_USER_MODEL,
                    verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('role', models.CharField(
                    choices=[('user', 'Пользователь'), ('moderator', 'Модератор'),
                             ('admin', 'Администратор')],
                    default='user', max_length=20, verbose_name='Роль')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='profile', to=settings.AUTH_USER_MODEL,
                    verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('email_notifications', models.BooleanField(
                    default=True, verbose_name='Уведомления на email')),
                ('items_per_page', models.PositiveSmallIntegerField(
                    default=10, verbose_name='Заявок на странице')),
                ('theme', models.CharField(
                    choices=[('light', 'Светлая'), ('dark', 'Тёмная')],
                    default='light', max_length=10, verbose_name='Тема')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='settings', to=settings.AUTH_USER_MODEL,
                    verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Настройки пользователя',
                'verbose_name_plural': 'Настройки пользователей',
            },
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=50, verbose_name='Поле')),
                ('old_value', models.CharField(blank=True, max_length=255,
                                               verbose_name='Старое значение')),
                ('new_value', models.CharField(blank=True, max_length=255,
                                               verbose_name='Новое значение')),
                ('changed_at', models.DateTimeField(auto_now_add=True, verbose_name='Когда')),
                ('ticket', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='history', to='tickets.ticket',
                    verbose_name='Заявка')),
                ('user', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL, verbose_name='Кто изменил')),
            ],
            options={
                'verbose_name': 'Изменение заявки',
                'verbose_name_plural': 'История изменений',
                'ordering': ['-changed_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments', to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор')),
                ('ticket', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments', to='tickets.ticket',
                    verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('request_id', models.CharField(blank=True, max_length=40,
                                                verbose_name='Request ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True,
                                                    verbose_name='IP-адрес')),
                ('user_agent', models.CharField(blank=True, max_length=300,
                                                verbose_name='User-Agent')),
                ('method', models.CharField(max_length=10, verbose_name='HTTP-метод')),
                ('path', models.CharField(max_length=300, verbose_name='Путь')),
                ('status_code', models.PositiveSmallIntegerField(
                    default=0, verbose_name='Код ответа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время')),
                ('user', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запись аудита',
                'verbose_name_plural': 'Audit log',
                'ordering': ['-created_at'],
            },
        ),
    ]
