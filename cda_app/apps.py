from django.apps import AppConfig

class CdaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cda_app'
    
    def ready(self):
        import cda_app.templatetags.custom_filters  # noqa
        import cda_app.templatetags.batch_filter