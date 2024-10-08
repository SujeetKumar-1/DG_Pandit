# Generated by Django 5.0.1 on 2024-03-31 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PanditJi', '0002_remove_pandit_name_remove_people_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='panditProfileData',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='PanditJi.pandit')),
                ('pname', models.CharField(max_length=155)),
                ('gender', models.CharField(max_length=55)),
                ('high_edu', models.CharField(max_length=55)),
                ('supp_docs', models.FileField(max_length=2048, upload_to='userImages/')),
                ('photo', models.ImageField(max_length=2048, upload_to='userImages/')),
                ('phone', models.IntegerField()),
                ('whatsapp', models.IntegerField()),
                ('country', models.CharField(max_length=155)),
                ('state', models.CharField(max_length=155)),
                ('city', models.CharField(max_length=155)),
                ('pincode', models.IntegerField()),
                ('faddress', models.TextField(max_length=500)),
                ('role', models.CharField(max_length=255)),
                ('experienc', models.IntegerField()),
                ('skill', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(max_length=700)),
                ('fee', models.IntegerField()),
                ('service_img', models.ImageField(max_length=2048, upload_to='serviceImages/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PanditJi.pandit')),
            ],
        ),
    ]
