# Generated by Django 4.0.6 on 2023-03-31 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0028_collabitem_collaboration'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='collaborations',
            field=models.ManyToManyField(blank=True, to='Teka.collaboration'),
        ),
    ]
