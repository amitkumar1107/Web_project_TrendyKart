# Generated by Django 5.1.5 on 2025-03-05 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_update', models.CharField(max_length=50)),
            ],
        ),
    ]
