# Generated by Django 3.2.5 on 2021-08-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pic',
            field=models.FileField(blank=True, null=True, upload_to='profile/'),
        ),
    ]