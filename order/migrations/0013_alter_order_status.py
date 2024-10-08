# Generated by Django 3.2.25 on 2024-09-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('paid', 'PAID'), ('payment failed', 'PAYMENT_FAILED'), ('dispatched', 'DISPATCHED'), ('delivered', 'DELIVERED'), ('cancelled', 'CANCELLED')], default='pending', max_length=20),
        ),
    ]
