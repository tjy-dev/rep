# Generated by Django 2.2.8 on 2019-12-16 07:40

import account.models
from django.db import migrations, models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_delete_userauthenticate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=250, null=True, verbose_name='bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=account.models.get_image_path, verbose_name='profile picture'),
        ),
    ]
