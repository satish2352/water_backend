# Generated by Django 4.0.6 on 2022-09-09 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0012_subscription_expired'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispensing_price', models.CharField(default=1000, max_length=255)),
                ('treatment_price', models.CharField(default=1200, max_length=255)),
                ('dispensing_tax', models.CharField(default=5, max_length=255)),
                ('treatment_tax', models.CharField(default=5, max_length=255)),
            ],
        ),
    ]
