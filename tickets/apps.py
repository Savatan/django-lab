from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'
    verbose_name = 'Заявки'

    def ready(self):
        from . import models  # noqa: F401  (регистрирует сигналы)
