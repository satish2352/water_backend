# Generated by Django 4.0.6 on 2022-08-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=0, verbose_name='email_verified'),
        ),
    ]
