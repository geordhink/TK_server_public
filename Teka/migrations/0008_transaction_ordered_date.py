# Generated by Django 4.0.6 on 2022-11-22 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0007_transaction_payment_method_transaction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
