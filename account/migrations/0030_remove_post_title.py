# Generated by Django 2.2.9 on 2019-12-31 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
