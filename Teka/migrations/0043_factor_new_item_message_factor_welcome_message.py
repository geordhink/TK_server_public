# Generated by Django 4.0.6 on 2024-02-17 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0042_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='new_item_message',
            field=models.CharField(default='Nouveau produit rien que pour vous !', max_length=400),
        ),
        migrations.AddField(
            model_name='factor',
            name='welcome_message',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
