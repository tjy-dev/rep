# Generated by Django 2.2.8 on 2019-12-13 12:08

import account.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20191213_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=account.models.get_image_path, verbose_name='profile picture'),
        ),
    ]
