from cms.app_base import CMSAppConfig


class DjangoTaxonomyCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_toolbar_enabled_admin = False
    cms_config_enabled = True
