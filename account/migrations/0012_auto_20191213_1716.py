# Generated by Django 2.2.8 on 2019-12-13 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20191213_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_pic2',
            new_name='profile_pic',
        ),
    ]
