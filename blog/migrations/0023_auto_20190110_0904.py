# Generated by Django 2.1.3 on 2019-01-10 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20190110_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mobileno',
            field=models.CharField(default='null', max_length=17),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobileno',
            field=models.CharField(default='+91 XXXX XXX XXX', max_length=17),
        ),
    ]