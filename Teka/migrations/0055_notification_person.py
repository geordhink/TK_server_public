# Generated by Django 4.0.6 on 2024-07-04 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0054_item_likers'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Teka.person'),
        ),
    ]
