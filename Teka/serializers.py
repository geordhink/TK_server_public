from rest_framework import serializers
from .models import *
from django_countries.serializers import CountryFieldMixin
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PersonSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = "__all__"

        
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class MiniPersonPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'profil']


class MiniFactorPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ['id', 'profil']

        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

        
class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ExchangeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"



class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = "__all__"


class CollabItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollabItem
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class TrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = "__all__"


