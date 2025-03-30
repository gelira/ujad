# Generated by Django 5.1.7 on 2025-03-30 20:39

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_rename_productorder_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.wallet'),
        ),
        migrations.CreateModel(
            name='ConsumingToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.UUIDField(blank=True, null=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expired_at', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
