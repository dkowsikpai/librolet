# Generated by Django 2.1.3 on 2019-01-19 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20190119_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='showpost',
            field=models.IntegerField(default=1),
        ),
    ]
