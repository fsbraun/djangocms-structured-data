from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoTaxonomyConfig(AppConfig):
    name = "djangocms_taxonomy"
    verbose_name = _("Taxonomy")
    default_auto_field = "django.db.models.BigAutoField"
