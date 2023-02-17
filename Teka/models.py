from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils.text import slugify

# from phonenumber_field.modelfields import PhoneNumberField

# final type
MEDIA_TYPE = (
    ('img', 'image'),
    ('vid', 'video'),
    ('aud', 'audio'),
    ('nan', 'else'),
)

ITEM_TYPE = (
    ('phy', 'physical'),
    ('vir', 'virtual'),
)


ITEM_STATE = (
    ('nw', 'New'),
    ('ud', 'Used'),
)


STATUS_TYPE = (
    ('I', 'Initial'),
    ('D', 'Done'),
    ('F', 'Failed'),
    ('W', 'Waiting'),
)

EXCHANGE_TYPE = (
    ('D', 'Depot'),
    ('R', 'Revocation'),
)

ITEM_CATEGORY = (
    ('hom', 'Home'),
    ('tec', 'Technology'),
    ('med', 'Media'),
    ('coo', 'Cook'),
    ('spo', 'Sport'),
    ('inf', 'Information'),
)

PAYEMENT_METHOD = (
    ('mtn', 'MTN Mobile money'),
    ('air', 'Airtel money'),
    ('ora', 'Orange money'),
    ('mas', 'MasterCard'),
    ('pay', 'Paypal'),
    ('str', 'Stripe'),
)


# Person
class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=True, null=True),
    last_name = models.CharField(max_length=255, blank=True, null=True),
    profil = models.ForeignKey('Profil', on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    # phone = PhoneNumberField(blank=True, null=True)
    born = models.DateTimeField(blank=True, null=True)
    total_amount = models.IntegerField(default=0)
    country = CountryField(blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user_name = self.user.username
        return super(Person, self).save(*args, **kwargs)


class Profil(models.Model):
    file_name = models.ImageField(upload_to='profils/%Y/%m/%d/')


class Media(models.Model):
    file_name = models.FileField(upload_to='medias/%Y/%m/%d/')
    type_file = models.CharField(max_length=3, choices=MEDIA_TYPE)

    def __str__(self):
        return f"{self.file_name}"


# market
class Item(models.Model):
    title = models.CharField(max_length=255)
    profils = models.ForeignKey(Profil, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item_type = models.CharField(max_length=4, choices=ITEM_TYPE)
    item_category = models.CharField(max_length=3, choices=ITEM_CATEGORY)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    rate = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=1)
    item_state = models.CharField(max_length=2, choices=ITEM_STATE, default='nw')


    def __str__(self):
        return f"{self.title} created at {self.created}"


class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=1, choices=STATUS_TYPE, default='I')
    payment_method = models.CharField(max_length=3, choices=PAYEMENT_METHOD, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def get_item_total_price(self):
        amount = 0
        if self.item.discount_price:
            amount = self.quantity * self.item.discount_price
        else:
            amount = self.quantity * self.item.price
        print(f"{self.quantity} {self.item.title}(s) gives {amount} Fcfa")
        return amount

    def __str__(self):
        return f"{self.quantity} {self.item.title}"


class Exchange(models.Model):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)
    exchange_type = models.CharField(max_length=1, choices=EXCHANGE_TYPE)
    status = models.CharField(max_length=1, choices=STATUS_TYPE, default='I')
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange {self.id} : {self.exchange_type} => {self.get_status_display()} ordered at {self.ordered_date} {self.person.user.username}"


class Factor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    profil = models.ForeignKey('Profil', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    slug = models.SlugField(editable=False, unique=True)
    items = models.ManyToManyField(Item, blank=True)
    transaction_done = models.ManyToManyField(Transaction, blank=True)
    clients_saved = models.ManyToManyField('Client', blank=True)
    followers = models.ManyToManyField('Client', related_name='followers')
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} owner by {self.person.user.username}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Factor, self).save(*args, **kwargs)


class Client(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    transactions = models.ManyToManyField(Transaction, blank=True)
    # items_bought = models.ManyToManyField(Item, blank=True)
    transactions_done = models.ManyToManyField(Transaction, related_name="after_payment_transactions", blank=True)
    payment_method = models.CharField(max_length=3, choices=PAYEMENT_METHOD)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.person.user.username} with {self.transactions.count()} transactions and {self.transactions_done.count()} transactions finished"

    def get_global_items_prices_in_cart(self):
        total = 0
        for transaction in self.transactions.all():
            total += transaction.get_item_total_price()
        print(f"{self.transactions.count()} item(s) for all gives {total} Fcfa")
        return total


class Try(models.Model):
    title = models.CharField(max_length=255)
    the_file = models.ImageField(upload_to='try-only/images', null=True, blank=True)

    def __str__(self):
        return self.title