# Generated by Django 5.1.6 on 2025-02-22 07:52

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_pet_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoorLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('direction', models.CharField(choices=[('in', 'In'), ('out', 'Out')], max_length=50)),
                ('status', models.CharField(choices=[('open', 'Open'), ('close', 'Close')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.pet')),
            ],
        ),
    ]
