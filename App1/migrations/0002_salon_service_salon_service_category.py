# Generated by Django 5.2.2 on 2025-07-07 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salon_Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('gender_specific', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex')], default='Unisex', max_length=50)),
                ('approved', models.BooleanField(default=False)),
                ('approved_by', models.CharField(blank=True, max_length=25, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.service_category')),
                ('created_branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.salonbranch')),
                ('created_salon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.salon')),
            ],
        ),
        migrations.CreateModel(
            name='Salon_Service_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_category_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('service_category_description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_by', models.CharField(blank=True, max_length=25, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.salonbranch')),
                ('created_salon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.salon')),
            ],
        ),
    ]
