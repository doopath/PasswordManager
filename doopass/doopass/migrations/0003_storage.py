# Generated by Django 5.0.2 on 2024-05-17 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doopass', '0002_rename_appuser_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doopass.user')),
            ],
        ),
    ]