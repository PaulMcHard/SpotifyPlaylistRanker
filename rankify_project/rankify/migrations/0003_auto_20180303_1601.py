# Generated by Django 2.0.2 on 2018-03-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankify', '0002_auto_20180227_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='spotifyUserURI',
            field=models.CharField(default=None, max_length=128, null=True, unique=True),
        ),
    ]