# Generated by Django 2.1.3 on 2019-01-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20190107_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostPicks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(default='default.jpg', upload_to='post_pics')),
            ],
        ),
        migrations.DeleteModel(
            name='PostPick',
        ),
    ]
