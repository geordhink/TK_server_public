# Generated by Django 4.0.6 on 2023-03-23 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0021_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='notifications',
            field=models.ManyToManyField(blank=True, to='Teka.notification'),
        ),
        migrations.AddField(
            model_name='person',
            name='notifications',
            field=models.ManyToManyField(blank=True, to='Teka.notification'),
        ),
    ]
