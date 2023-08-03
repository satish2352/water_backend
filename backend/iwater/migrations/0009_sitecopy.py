# Generated by Django 4.0.6 on 2022-08-31 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0008_user_token_user_token_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=60, null=True)),
                ('phone_verified', models.BooleanField(default=0, verbose_name='phone_verified')),
                ('status', models.BooleanField(default=True)),
                ('alerts', models.SmallIntegerField(default=0)),
                ('created', models.DateField(auto_now_add=True)),
                ('is_treatment_unit', models.BooleanField(default=False, verbose_name='Is treatment')),
                ('is_dispensing_unit', models.BooleanField(default=False, verbose_name='Is dispensing')),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('otp_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sitecopy_company', to='iwater.company', verbose_name='sitecopy_company')),
            ],
        ),
    ]
