# Generated by Django 3.2.9 on 2021-12-20 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paintball', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='uploads'),
        ),
    ]
