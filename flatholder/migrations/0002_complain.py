# Generated by Django 3.2.5 on 2021-09-11 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flatholder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=50)),
                ('dis', models.TextField()),
                ('creted_on', models.DateTimeField(auto_now_add=True)),
                ('cpic', models.FileField(blank=True, null=True, upload_to='Complain')),
                ('status', models.CharField(default='OPEN', max_length=50)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flatholder.userf')),
            ],
        ),
    ]
