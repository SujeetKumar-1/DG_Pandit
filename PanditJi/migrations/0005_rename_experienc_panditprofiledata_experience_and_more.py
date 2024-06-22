# Generated by Django 5.0.1 on 2024-04-02 08:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PanditJi', '0004_rename_services_servicedata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='panditprofiledata',
            old_name='experienc',
            new_name='experience',
        ),
        migrations.AddField(
            model_name='panditprofiledata',
            name='lang',
            field=models.TextField(default=django.utils.timezone.now, max_length=155),
            preserve_default=False,
        ),
    ]
