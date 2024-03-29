# Generated by Django 4.0.6 on 2023-03-22 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0020_factor_collab_guest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('opened', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
