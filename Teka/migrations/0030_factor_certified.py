# Generated by Django 4.0.6 on 2023-03-31 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0029_factor_collaborations'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='certified',
            field=models.BooleanField(default=False),
        ),
    ]
