# Generated by Django 3.1.5 on 2021-01-22 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='q10',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='q8',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='q9',
            field=models.BooleanField(default=False),
        ),
    ]
