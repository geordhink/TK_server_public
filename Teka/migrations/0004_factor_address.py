# Generated by Django 4.0.6 on 2022-08-18 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0003_remove_person_to_see'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='address',
            field=models.CharField(default='Brazza Quater', max_length=255),
            preserve_default=False,
        ),
    ]
