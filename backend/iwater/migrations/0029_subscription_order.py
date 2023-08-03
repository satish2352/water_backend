# Generated by Django 4.0.6 on 2022-10-06 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iwater', '0028_alter_order_paid_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_id', to='iwater.order', verbose_name='order_id'),
        ),
    ]
