# Generated by Django 4.0.6 on 2022-09-23 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0021_user_added_by'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='site',
            unique_together={('site_name', 'company')},
        ),
        migrations.AlterModelTable(
            name='site',
            table='iwater_site',
        ),
    ]
