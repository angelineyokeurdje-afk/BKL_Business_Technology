from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Comptes utilisateurs'

    def ready(self):
        """Charge les signaux pour la création automatique du profil."""
        import accounts.models  # noqa — déclenche post_save signals
