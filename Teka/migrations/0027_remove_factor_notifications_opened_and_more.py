# Generated by Django 4.0.6 on 2023-03-25 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0026_alter_factor_notifications_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='notifications_opened',
        ),
        migrations.RemoveField(
            model_name='person',
            name='notifications_opened',
        ),
        migrations.AddField(
            model_name='factor',
            name='notifications_not_opened',
            field=models.ManyToManyField(blank=True, related_name='notifications_factor_not_opened', to='Teka.notification'),
        ),
        migrations.AddField(
            model_name='person',
            name='notifications_not_opened',
            field=models.ManyToManyField(blank=True, related_name='notifications_person_not_opened', to='Teka.notification'),
        ),
    ]
