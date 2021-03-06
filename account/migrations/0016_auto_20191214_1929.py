# Generated by Django 2.2.8 on 2019-12-14 10:29

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20191213_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.get_image_path, verbose_name='profile picture'),
        ),
    ]
