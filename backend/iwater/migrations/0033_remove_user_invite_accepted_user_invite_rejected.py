# Generated by Django 4.0.6 on 2022-10-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0032_user_invite_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='invite_accepted',
        ),
        migrations.AddField(
            model_name='user',
            name='invite_rejected',
            field=models.BooleanField(default=0, verbose_name='invite_rejected'),
        ),
    ]
