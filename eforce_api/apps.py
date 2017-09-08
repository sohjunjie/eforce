from django.apps import AppConfig


class EforceApiConfig(AppConfig):
    name = 'eforce_api'

    def ready(self):
        import eforce_api.signals
