from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    home_town = models.CharField(_("home town"), max_length=120)
    location = models.CharField(_("current location"), max_length=120)
    birth_date = models.DateField(_("birth date"))
    phone = models.CharField(_("phone number"), max_length=64)
    email = models.EmailField(_("email address"), unique=True)
    default_job_title = models.CharField(_("default job title"), max_length=120)
    is_main_profile = models.BooleanField(default=False, editable=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]


class SocialLink(models.Model):
    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="social_links"
    )
    title = models.CharField(_("title"), max_length=120)
    link = models.CharField(_("link"), max_length=120)
