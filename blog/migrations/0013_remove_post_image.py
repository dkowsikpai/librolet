# Generated by Django 2.1.3 on 2019-01-07 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
