# Generated by Django 2.2.8 on 2019-12-09 12:14

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.get_image_path),
        ),
    ]
