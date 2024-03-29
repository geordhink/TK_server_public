# Generated by Django 4.0.6 on 2023-03-31 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0027_remove_factor_notifications_opened_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollabItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_collab', models.FloatField(blank=True, null=True)),
                ('stock_collab', models.IntegerField(blank=True, null=True)),
                ('percent_item', models.FloatField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Teka.item')),
            ],
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collab_date', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
                ('percent', models.FloatField(default=15.0)),
                ('collab_items', models.ManyToManyField(to='Teka.collabitem')),
                ('factor_asker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Teka.factor')),
            ],
        ),
    ]
