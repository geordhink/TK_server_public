# Generated by Django 4.0.6 on 2023-05-12 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teka', '0038_rename_stock_collab_collabitem_sale'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collabitem',
            old_name='sale',
            new_name='item_sales',
        ),
    ]