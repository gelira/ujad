# Generated by Django 5.1.7 on 2025-03-21 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_productticket_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='payment_method',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
