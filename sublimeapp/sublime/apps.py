from django.apps import AppConfig


class SublimeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sublime'

    def ready(self):
        import sublime.signals
        
        