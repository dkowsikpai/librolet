# Generated by Django 2.1.3 on 2019-01-20 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_auto_20190120_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='email',
            field=models.EmailField(default='No Email', max_length=300),
        ),
        migrations.AlterField(
            model_name='post',
            name='mobileno',
            field=models.CharField(default='No Mob', max_length=17),
        ),
    ]