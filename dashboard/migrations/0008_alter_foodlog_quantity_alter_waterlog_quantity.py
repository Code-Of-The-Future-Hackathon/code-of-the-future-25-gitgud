# Generated by Django 5.1.6 on 2025-02-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_foodlog_waterlog_delete_foodwaterlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodlog',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='waterlog',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
