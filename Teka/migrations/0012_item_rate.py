# Generated by Django 4.0.6 on 2022-12-26 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0011_exchange_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='rate',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
