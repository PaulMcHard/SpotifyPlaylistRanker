# Generated by Django 2.0.2 on 2018-03-05 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankify', '0005_auto_20180305_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='spotify_username',
            field=models.CharField(default=None, max_length=128),
        ),
    ]