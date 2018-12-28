from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CMSAppConfig(AppConfig):
    name = "cms"
    verbose_name = _("Content Management System")
