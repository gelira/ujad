# Generated by Django 5.1.7 on 2025-03-22 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_alter_authcode_user'),
        ('sales', '0004_ticket_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productticket',
            name='dispatcher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='custom_auth.user'),
        ),
    ]
