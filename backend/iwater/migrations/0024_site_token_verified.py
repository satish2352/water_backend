# Generated by Django 4.0.6 on 2022-10-03 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0023_alter_site_phone_alter_site_site_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='token_verified',
            field=models.BooleanField(default=0, verbose_name='token_verified'),
        ),
    ]
