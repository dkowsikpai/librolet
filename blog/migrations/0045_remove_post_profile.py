# Generated by Django 2.1.7 on 2019-03-14 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='profile',
        ),
    ]
