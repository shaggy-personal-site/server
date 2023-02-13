from datetime import date

from dirtyfields import DirtyFieldsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models


class Project(models.Model, DirtyFieldsMixin):
    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(_("Title"), max_length=120)
    description = models.TextField(_("Description"), null=True, blank=True)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if "finished" in self.get_dirty_fields() and self.finished and not self.end:
            self.end = date.today()
        self.finished = bool(self.end)
        super().save(*args, **kwargs)
