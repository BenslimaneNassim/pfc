from django.apps import AppConfig


class VintageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vintage'
    def ready(self):
        import vintage.signals  # import the signals module
