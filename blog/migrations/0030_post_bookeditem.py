# Generated by Django 2.1.3 on 2019-01-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20190119_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookeditem',
            field=models.IntegerField(default=0),
        ),
    ]