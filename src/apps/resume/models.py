from datetime import date

from dateutil.relativedelta import relativedelta
from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    title = models.CharField(_("title"), max_length=120)


class Job(models.Model, DirtyFieldsMixin):
    company = models.ForeignKey(
        "companies.Company", on_delete=models.PROTECT, related_name="employees_job"
    )
    resume = models.ForeignKey(
        "resume.Resume", on_delete=models.CASCADE, related_name="jobs"
    )
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if "finished" in self.get_dirty_fields() and self.finished and not self.end:
            self.end = date.today()
        self.finished = bool(self.end)
        super().save(*args, **kwargs)


class Education(models.Model):
    title = models.CharField(max_length=120)
    resume = models.ForeignKey(
        "resume.Resume", on_delete=models.CASCADE, related_name="education_set"
    )
    start = models.DateField()
    end = models.DateField()


class Resume(models.Model, DirtyFieldsMixin):
    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="resumes"
    )
    title = models.CharField(_("Title"), max_length=120)
    projects = models.ManyToManyField("projects.Project", related_name="resumes")
    skills = models.ManyToManyField("resume.Skill", related_name="resumes")

    @property
    def experience(self) -> str:
        # TODO: compare the execution speed diff between aggregate and latest/earliest queries
        date_range = self.jobs.aggregate(models.Min("start"), models.Max("end"))
        start, end = date_range["start__min"], date_range["end__max"]
        exp = relativedelta(end, start)

        return ", ".join(
            [
                f"{field}: {getattr(exp, field)}"
                for field in ("years", "months", "days")
                if getattr(exp, field)
            ]
        )
