# Generated by Django 2.0.2 on 2018-03-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankify', '0011_auto_20180312_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='playlist_image_url',
            field=models.CharField(default='none', max_length=128),
        ),
    ]
