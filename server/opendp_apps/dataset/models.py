from django.core.files.storage import FileSystemStorage

from django.db import models
from django.db.models import CASCADE
from django.conf import settings
from polymorphic.models import PolymorphicModel

from opendp_apps.model_helpers.models import \
    (TimestampedModelWithUUID,)


UPLOADED_FILE_STORAGE = FileSystemStorage(location=settings.UPLOADED_FILE_STORAGE_ROOT)


class DataSetInfo(TimestampedModelWithUUID, PolymorphicModel):
    """
    Base type for table that either holds DV data
    or a file upload
    """
    name = models.CharField(max_length=128)

    # user who initially added/uploaded data
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.PROTECT)

    class SourceChoices(models.TextChoices):
        UserUpload = 'upload', 'Upload'
        Dataverse = 'dataverse', 'Dataverse'

    source = models.CharField(max_length=128,
                              choices=SourceChoices.choices)

    # Redis key to store potentially sensitive information
    # during analysis setup
    data_profile_key = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = 'Dataset Information'
        verbose_name_plural = 'Dataset Information'
        ordering = ('name', '-created')

    def __str__(self):
        return self.name



class DataverseFileInfo(DataSetInfo):
    """
    Refers to a DV file from within a DV dataset
    """
    # TODO: This should have all fields from DV API response
    dataverse_file_id = models.IntegerField()
    doi = models.CharField(max_length=128)
    installation_name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Dataverse File Information'
        verbose_name_plural = 'Dataverse File Information'
        ordering = ('name', '-created')

    def __str__(self):
        return f'{self.name} ({self.installation_name})'

    def save(self, *args, **kwargs):
        # Future: is_complete can be auto-filled based on either field values or the STEP
        #   Note: it's possible for either variable_ranges or variable_categories to be empty, e.g.
        #       depending on the data
        #
        self.source = DataSetInfo.SourceChoices.Dataverse
        super(DataverseFileInfo, self).save(*args, **kwargs)



class UploadFileInfo(DataSetInfo):
    """
    Refers to a file uploaded independently of DV
    """

    # user uploaded files, keep them off of the web path
    #
    data_file = models.FileField('User uploaded files',
                    storage=UPLOADED_FILE_STORAGE,
                    upload_to='user-files/%Y/%m/%d/')

    def save(self, *args, **kwargs):
        # Future: is_complete can be auto-filled based on either field values or the STEP
        #   Note: it's possible for either variable_ranges or variable_categories to be empty, e.g.
        #       depending on the data
        #
        self.source = DataSetInfo.SourceChoices.UserUpload
        super(UploadFileInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Upload File Information'
        verbose_name_plural = 'Upload File Information'
        ordering = ('name', '-created')

    def __str__(self):
        return f'{self.name} ({self.source})'
