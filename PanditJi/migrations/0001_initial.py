# Generated by Django 5.0.1 on 2024-03-04 03:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_type', models.CharField(choices=[('SUPERUSER', 'superuser'), ('PEOPLE', 'people'), ('PANDIT', 'pandit')], default='SUPERUSER', max_length=10)),
                ('UID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_people', models.BooleanField(default=False)),
                ('is_pandit', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pandit',
            fields=[
                ('useraccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=72)),
            ],
            options={
                'abstract': False,
            },
            bases=('PanditJi.useraccount',),
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('useraccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=72)),
            ],
            options={
                'abstract': False,
            },
            bases=('PanditJi.useraccount',),
        ),
    ]
