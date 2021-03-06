from django.db import models
from django.conf import settings
from opendp_apps.dataset.models import DataSetInfo
from opendp_apps.model_helpers.models import \
    (TimestampedModel, TimestampedModelWithUUID)


class TermsOfAccess(TimestampedModel):
    """
    Terms of Access Content
    """
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    description = models.TextField()
    version = models.FloatField(null=False, blank=False)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Terms of Access'
        verbose_name_plural = 'Terms of Access'
        ordering = ('active', 'name',)

    def __str__(self):
        return self.name


class TermsOfAccessLog(TimestampedModelWithUUID):
    """
    Log of Terms of Access
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    dataset_info = models.ForeignKey(DataSetInfo, on_delete=models.PROTECT)
    terms_of_access = models.ForeignKey(TermsOfAccess, on_delete=models.PROTECT)

    verbose_name = 'Terms of Access Log'
    verbose_name_plural = 'Terms of Access Logs'
    ordering = ('-created', 'user')

    def __str__(self):
        return f'{self.user} - {self.dataset_info}'
