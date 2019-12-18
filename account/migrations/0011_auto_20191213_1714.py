# Generated by Django 2.2.8 on 2019-12-13 08:14

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20191213_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic2',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.get_image_path),
        ),
    ]
