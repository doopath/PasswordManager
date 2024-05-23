# Generated by Django 5.0.2 on 2024-05-23 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doopass', '0012_alter_backup_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backup',
            name='content',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='backup',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doopass.storage'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='content',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='storage',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]