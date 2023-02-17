# Generated by Django 4.0.6 on 2022-08-16 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('mtn', 'MTN Mobile money'), ('air', 'Airtel money'), ('ora', 'Orange money'), ('mas', 'MasterCard'), ('pay', 'Paypal'), ('str', 'Stripe')], max_length=3)),
                ('billing_address', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('item_type', models.CharField(choices=[('phy', 'physical'), ('vir', 'virtual')], max_length=4)),
                ('item_category', models.CharField(choices=[('hom', 'Home'), ('tec', 'Technology'), ('med', 'Media'), ('coo', 'Cook'), ('spo', 'Sport'), ('inf', 'Information')], max_length=3)),
                ('price', models.IntegerField()),
                ('discount_price', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stock', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='medias/%Y/%m/%d/')),
                ('type_file', models.CharField(choices=[('img', 'image'), ('vid', 'video'), ('aud', 'audio'), ('nan', 'else')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.ImageField(upload_to='profils/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Try',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Teka.item')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('born', models.DateTimeField(blank=True, null=True)),
                ('total_amount', models.IntegerField(default=0)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('profil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Teka.profil')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Teka.media'),
        ),
        migrations.AddField(
            model_name='item',
            name='profils',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Teka.profil'),
        ),
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('total_amount', models.IntegerField(default=0)),
                ('clients_saved', models.ManyToManyField(blank=True, to='Teka.client')),
                ('items', models.ManyToManyField(blank=True, to='Teka.item')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Teka.person')),
                ('profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Teka.profil')),
                ('transaction_done', models.ManyToManyField(blank=True, to='Teka.transaction')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='items_bought',
            field=models.ManyToManyField(blank=True, to='Teka.item'),
        ),
        migrations.AddField(
            model_name='client',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Teka.person'),
        ),
        migrations.AddField(
            model_name='client',
            name='transactions',
            field=models.ManyToManyField(blank=True, to='Teka.transaction'),
        ),
    ]
