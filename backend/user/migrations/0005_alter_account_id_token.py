# Generated by Django 3.2.9 on 2021-12-26 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20211225_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id_token',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
