# Generated by Django 2.0.2 on 2018-03-12 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankify', '0012_playlist_playlist_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='slug',
            field=models.SlugField(default='none'),
        ),
    ]
