# Generated by Django 2.2.9 on 2020-01-13 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_auto_20200113_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likePost',
        ),
    ]
