# Generated by Django 5.2.2 on 2025-06-19 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0004_alter_user_branches'),
    ]

    operations = [
        migrations.CreateModel(
            name='Superadmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
