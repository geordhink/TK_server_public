# Generated by Django 4.0.6 on 2023-05-06 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0035_remove_factor_collab_guest_factor_collab_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='items_collaboration',
            field=models.ManyToManyField(blank=True, related_name='items_to_resell', to='Teka.item'),
        ),
    ]