# Generated by Django 2.1.3 on 2019-01-22 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_auto_20190122_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='post_id',
            field=models.IntegerField(default=0),
        ),
    ]
