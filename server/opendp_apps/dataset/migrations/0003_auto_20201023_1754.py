# Generated by Django 3.1.2 on 2020-10-23 17:54

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_auto_20201022_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfileinfo',
            name='data_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/code/server/test_setup/user_uploaded_data'), upload_to='user-files/%Y/%m/%d/', verbose_name='User uploaded files'),
        ),
    ]
