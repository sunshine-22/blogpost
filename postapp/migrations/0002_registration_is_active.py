# Generated by Django 4.0.1 on 2022-03-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
