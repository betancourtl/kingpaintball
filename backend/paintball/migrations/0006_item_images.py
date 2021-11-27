# Generated by Django 3.2.9 on 2021-11-27 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paintball', '0005_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='images',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='item_images', to='paintball.image'),
            preserve_default=False,
        ),
    ]
