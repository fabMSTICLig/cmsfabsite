# Generated by Django 4.2.9 on 2024-03-13 07:47

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SingleTokenAccess',
            fields=[
                ('slug', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('contact', models.EmailField(max_length=100)),
                ('token', models.CharField(default=core.models.SingleTokenAccess.token_default, max_length=50)),
            ],
        ),
    ]
