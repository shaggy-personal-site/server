from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    title = models.CharField(_("name of company"), max_length=120)
    description = models.TextField(_("description of company"))
    location = models.CharField(_("location"), max_length=120)
