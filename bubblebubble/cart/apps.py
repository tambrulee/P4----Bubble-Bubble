from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        # Import signals so user_logged_in receiver is registered
        import cart.signals  # noqa
