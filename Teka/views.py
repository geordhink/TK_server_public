from random import randrange

import django
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework.viewsets import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
# social allauth importation
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# # ####### registration and login section #######
class RegisterUser(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializers = RegisterSerializer(all_users, many=True)
        return Response(serializers.data, status=HTTP_200_OK)

    def post(self, request):
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(request)
            user = User.objects.get(
                Q(username=serializers.data['username']) |
                Q(email=serializers.data['email'])
            )
            person = Person.objects.create(user_id=user.id)
            # client = Client.objects.create(person_id=person.id)
            # print(client)
            token = TokenModel.objects.create(user=user)
            token_serializers = TokenSerializer(token)
            return Response(token_serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)


# ####### globals viewsets section #######
class PersonsViewSet(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class ProfilViewSet(ModelViewSet):
    serializer_class = ProfilSerializer
    queryset = Profil.objects.all()
    # permission


class MediaViewSet(ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()


class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.order_by('-created')


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.order_by('-ordered_date')


class FactorViewSet(ModelViewSet):
    serializer_class = FactorSerializer
    queryset = Factor.objects.all()


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.order_by('-pub_date')


class CollaborationViewSet(ModelViewSet):
    serializer_class = CollaborationSerializer
    queryset = Collaboration.objects.order_by('-collab_date')


# ####### social networks registration section #######
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


# ####### persons section #######
class GetLoginByToken(APIView):
    def get(self, request, key):
        token = get_object_or_404(TokenModel, key=key)
        user = User.objects.get(id=token.user_id)
        serializers = UserSerializer(user)
        return Response(serializers.data, status=HTTP_200_OK)


class GetPersonByUserId(APIView):
    def get(self, request, user_id):
        person = get_object_or_404(Person, user_id=user_id)
        serializers = PersonSerializer(person)
        return Response(serializers.data, status=HTTP_200_OK)


# ####### markets section #######
class GlobalSearch(APIView):
    def get(self, request, search_word):
        item_result = Item.objects.filter(Q(title__icontains=search_word))
        factor_result = Factor.objects.filter(Q(title__icontains=search_word))
        if item_result:
            serializers = ItemSerializer(item_result, many=True)
            return Response(serializers.data, status=HTTP_200_OK)
        else:
            serializers = FactorSerializer(factor_result, many=True)
            return Response(serializers.data, status=HTTP_200_OK)


class RetrieveFactorItemsSearch(APIView):
    def get(self, request, factor_id, searched_text):
        factor = get_object_or_404(Factor, id=factor_id)
        items = factor.items.filter(title__contains=searched_text)
        serializers = ItemSerializer(items, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class GetFactorByPerson(APIView):
    def get(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        factor = get_object_or_404(Factor, person=person)
        serializers = FactorSerializer(factor)
        return Response(serializers.data, status=HTTP_200_OK)


class GetClientByPerson(APIView):
    def get(self, request, person_id):
        person = get_object_or_404(Person, id=person_id)
        client = get_object_or_404(Client, person=person)
        serializers = ClientSerializer(client)
        return Response(serializers.data, status=HTTP_200_OK)


class GetTransactionByItem(APIView):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        transaction = get_object_or_404(Transaction, item=item)
        serializers = TransactionSerializer(transaction)
        return Response(serializers.data, status=HTTP_200_OK)


class GetClientTransactions(APIView):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        all_transactions = client.transactions.all()
        serializers = TransactionSerializer(all_transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class GetOrCreatePersonClient(APIView):
    def get(self, request, person_id):
        client = Client.objects.get_or_create(person_id=person_id)
        serializers = ClientSerializer(client[0])
        return Response(serializers.data, status=HTTP_200_OK)
        # if client[1]:
        #     serializers = ClientSerializer(client[0])
        #     return Response(serializers.data, status=HTTP_200_OK)
        # else:
        #     serializers = ClientSerializer(client[0])
        #     return Response(serializers.data, status=HTTP_200_OK)


class AddItemToFactor(APIView):
    def get(self, request, factor_id):
        factor = get_object_or_404(Factor, id=factor_id)
        item = get_object_or_404(Item, id=request.id)
        serializers = FactorSerializer(factor)
        return Response(serializers.data, status=HTTP_200_OK)

    def post(self, request, factor_id):
        factor = get_object_or_404(Factor, id=factor_id)
        serializers = itemSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            factor.items.add(serializers)
            return Response(serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)


def get_item_factor(request, item_id):
    factor = Factor.objects.get(items=item_id)
    serializers = FactorSerializer(factor)
    return JsonResponse(serializers.data, status=200)


class UpdateOrCreateClientTransactionByItem(APIView):
    def get(self, request, person_id, item_id, quantity):
        # client = get_object_or_404(Client, id=person_id)
        client_check = Client.objects.get_or_create(person_id=person_id)
        client = client_check[0]
        item = get_object_or_404(Item, id=item_id)
        transaction_tuple = client.transactions.get_or_create(item=item)
        transaction_tuple[0].quantity = quantity
        transaction_tuple[0].save()
        client.save()
        serializers = ClientSerializer(client)
        return Response(serializers.data, status=HTTP_200_OK)


class ClientTransaction(APIView):
    def get(self, client_id, item_id):
        client = get_object_or_404(Client, id=client_id)
        try:
            transaction = client.transactions.get(item_id=item_id)
        except:
            transaction = client.transactions.create(item_id)
            transaction.save()
        if type(transaction) == tuple:
            serializers = TransactionSerializer(transaction[0])
        client.save()
        serializers = TransactionSerializer(transaction)
        return Response(serializers.data, status=HTTP_200_OK)


class GetAllFactorItems(APIView):
    def get(self, request, factor_id):
        factor = get_object_or_404(Factor, id=factor_id)
        all_items = factor.items.order_by('-created')
        serializers = ItemSerializer(all_items, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class ClientBuyItemByTransaction(APIView):
    def get(self, request, client_id, item_id=None):
        client = get_object_or_404(Client, id=client_id)
        all_transactions = client.transactions.all()
        serializers = TransactionSerializer(all_transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)

    def post(self, request, client_id, item_id):
        client = get_object_or_404(Client, id=client_id)
        item = get_object_or_404(Item, id=item_id)
        transaction = client.transactions.get_or_create(item=item)
        if transaction[1]:
            serializers = TransactionSerializer(transaction[0])
            if serializers.is_valid():
                serializers.save()
                item.save()
                return Response(serializers.data, status=HTTP_201_CREATED)
            return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return redirect(f'/viewsets/transactions/{transaction[0].id}/')


def remove_one_transaction_of_client(request, client_id, item_id):
    client = get_object_or_404(Client, id=client_id)
    transaction = client.transactions.get(item_id=item_id)
    client.transactions.remove(transaction)
    serializers = ClientSerializer(client)
    return JsonResponse(serializers.data, status=200)


def remove_all_transaction_of_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    for t in client.transactions.all():
        client.transactions.remove(t)
    client.save()
    serializers = ClientSerializer(client)
    return JsonResponse(serializers.data, safe=False)


class GetPhysicalItems(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.filter(item_type='phy').order_by('-created')


class GetVirtualItems(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.filter(item_type='vir').order_by('-created')


class GetLastCreatedItems(APIView):
    def get(self, request):
        now = timezone.now() - timedelta(days=31)
        all_items = Item.objects.filter(created__gte=now).order_by('-created')
        serializers = ItemSerializer(all_items, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


def get_person_s_factory(request, person_id):
    factory = get_object_or_404(Factor, person_id=person_id)
    serializers = FactorSerializer(factory)
    return JsonResponse(serializers.data, status=200)


class CreateThenAddItemInFactor(APIView):
    def post(self, request, factor_id):
        factor = get_object_or_404(Factor, id=factor_id)
        serializers = ItemSerializer(data=request.data)
        print(f"request data => {request.data}")
        if serializers.is_valid():
            serializers.save()
            factor.items.add(serializers.data['id'])
            return Response(serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, factor_id):
        factor = get_object_or_404(Factor, id=factor_id)
        serializers = ItemSerializer(data=request.data)
        print(f"request data updated => {request.data}")
        if serializers.is_valid():
            serializers.update()
            factor.items.update(serializers.data['id'])
            return Response(serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)


class UpdateItemInFactorAPIView(APIView):
    def put(self, request, factor_id):
        factor = get_object_or_404(Factor, id=factor_id)
        serializers = ItemSerializer(data=request.data)
        print(f"request data updated => {request.data}")
        if serializers.is_valid():
            serializers.update()
            factor.items.update(serializers.data['id'])
            return Response(serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)


def add_person_amount(request, person_id, amount):
    if request.method == 'GET':
        person = get_object_or_404(Person, id=person_id)
        person.total_amount += amount
        person.save()
        serializers = PersonSerializer(person)
        exchange = Exchange.objects.create(
            person=person,
            amount=amount,
            exchange_type='D',
            status='F'
        )
        return JsonResponse(serializers.data, status=200, safe=False)


class PayCartItems(APIView):
    def get(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        person = get_object_or_404(Person, pk=client.person.id)
        for transaction in client.transactions.all():
            if person.total_amount < client.get_global_items_prices_in_cart() or transaction.item.stock < transaction.quantity:
                transaction.status = 'F'
                transaction.save()
                factor = Factor.objects.get(items=transaction.item.id)
                factor.transaction_done.add(transaction)
                factor.save()
                client.transactions_done.add(transaction)
                client.save()
                # serializers = TransactionSerializer(transaction)
                serializers = ClientSerializer(client)
                return Response(serializers.data, status=HTTP_400_BAD_REQUEST)
            transaction.item.stock -= transaction.quantity
            transaction.item.save()
            client.transactions.remove(transaction)
            transaction.status = 'D'
            client.transactions_done.add(transaction)
            factor = Factor.objects.get(items=transaction.item.id)
            factor.transaction_done.add(transaction)
            factor.clients_saved.add(client)
            factor.total_amount += transaction.get_item_total_price()
            person.total_amount -= transaction.get_item_total_price()
            # notification with transaction
            notification = Notification.objects.create(
                message=f"La transaction {transaction.id}, a été effectué avec succès.",
                transaction=transaction,
            )
            notification.save()
            person.notifications_not_opened.add(notification)
            factor.notifications_not_opened.add(notification)
            transaction.save()
            factor.save()
        client.save()
        person.save()
        serializers = ClientSerializer(client)
        return Response(serializers.data, status=HTTP_200_OK)


class RetrieveOneClientByTransactionAPIView(APIView):
    def get(self, request, factor_id, transaction_id):
        factor = get_object_or_404(Factor, id=factor_id)
        transaction = factor.transaction_done.get(id=transaction_id)
        client = factor.clients_saved.get(transactions_done=transaction)
        person = get_object_or_404(Person, id=client.person.id)
        serializers = PersonSerializer(person)
        return Response(serializers.data, status=HTTP_200_OK)


class RetrieveAllItemsBoughtByClientAPIView(APIView):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        items_bought = []
        client_transactions_done = client.transactions_done.exclude(status='F').order_by('-ordered_date')
        for transaction in client_transactions_done:
            if transaction.item in items_bought:
                # print("already in list.")
                pass
            else:
                items_bought.append(transaction.item)
        # print(items_bought)
        serializers = ItemSerializer(items_bought, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class ThirdLastTransactionsByClientAPIView(APIView):
    def get(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        transactions = client.transactions_done.order_by("-ordered_date")[:3]
        serializers = TransactionSerializer(transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class ThirdLastTransactionsByFactorAPIView(APIView):
    def get(self, request, factor_id):
        factor = get_object_or_404(Factor, pk=factor_id)
        transactions = factor.transaction_done.order_by("-ordered_date")[:3]
        serializers = TransactionSerializer(transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class ThirdLastTransactionsFactorClientByPersonAPIView(APIView):
    def get(self, request, person_id):
        transactions = Transaction.objects.filter(Q(factor__person_id=person_id) or Q(client__person_id=person_id)).order_by('-ordered_date')[:3]
        serializers = TransactionSerializer(transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class ThirdLastClientsByFactorAPIView(APIView):
    def get(self, request, factor_id):
        factor = get_object_or_404(Factor, pk=factor_id)
        clients = factor.clients_saved.all() #.order_by('-transactions_done__ordered_date')
        c_list = []
        t_list = []
        for c in clients:
            for t in c.transactions_done.filter(status='D').order_by('-ordered_date'):
                if t in t_list:
                    pass
                else:
                    t_list.append(t)
        serializers = TransactionSerializer(transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class RetrieveAllTransactionsDoneByClientAPIView(APIView):
    def get(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        transactions = client.transactions_done.all().order_by("-ordered_date")
        serializers = TransactionSerializer(transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class RetrieveOneItemAllTransactionsDoneAPIView(APIView):
    def get(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        all_transactions = item.transaction_set.filter(status='D')
        serializers = TransactionSerializer(all_transactions, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class ListAllRandomItemsByTypeAPIView(APIView):
    def get(self, request, type_str):
        all_items = Item.objects.filter(item_type__contains=type_str)
        items_rd = []
        for i in all_items:
            if (all_items[randrange(len(all_items))]) in items_rd:
                pass
            else:
                items_rd.append(all_items[randrange(len(all_items))])
        serializers = ItemSerializer(items_rd, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


def get_flux_factors_transactions(request, person_id, flux):
    try:
        factor = get_object_or_404(Factor, person_id=person_id)
        client = get_object_or_404(Client, person_id=person_id)
        if flux == 'input':
            transactions = factor.transaction_done.order_by('-ordered_date')
            serializers = TransactionSerializer(transactions, many=True)
            return JsonResponse(serializers.data, safe=False)

        if flux == 'output':
            transactions = client.transactions_done.order_by('-ordered_date')
            serializers = TransactionSerializer(transactions, many=True)
            return JsonResponse(serializers.data, safe=False)
    finally:
        if flux == 'output':
            client = get_object_or_404(Client, person_id=person_id)
            transactions = client.transactions_done.order_by('-ordered_date')
            serializers = TransactionSerializer(transactions, many=True)
            return JsonResponse(serializers.data, safe=False)


def get_flux_factors_transactions_status(request, person_id, flux, status='D'):
    try:
        factor = get_object_or_404(Factor, person_id=person_id)
        client = get_object_or_404(Client, person_id=person_id)
        if flux == 'input':
            transactions = factor.transaction_done.filter(status=status).order_by('-ordered_date')
            serializers = TransactionSerializer(transactions, many=True)
            return JsonResponse(serializers.data, safe=False)

        if flux == 'output':
            transactions = client.transactions_done.filter(status=status).order_by('-ordered_date')
            serializers = TransactionSerializer(transactions, many=True)
            return JsonResponse(serializers.data, safe=False)
    finally:
        client = get_object_or_404(Client, person_id=person_id)
        if flux == 'output':
            transactions = client.transactions_done.filter(status=status).order_by('-ordered_date')
            serializers = TransactionSerializer(transactions, many=True)
            return JsonResponse(serializers.data, safe=False)


def follow_action_client_factor(request, client_id, factor_id):
    client = get_object_or_404(Client, pk=client_id)
    factor = get_object_or_404(Factor, pk=factor_id)
    if client in factor.followers.all():
        factor.followers.remove(client)
    else:
        factor.followers.add(client)
    serializers = FactorSerializer(factor)
    return JsonResponse(serializers.data, safe=False)


class RegisterNewFactor(APIView):
    def get(self, request):
        all_factors = Factor.objects.all()
        serializers = FactorSerializer(all_factors, many=True)
        return Response(serializers.data, status=HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializers = FactorSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)


def deposit_exchange(request, person_id, amount):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'GET':
        all_exchanges = Exchange.objects.all()
        serializers = ExchangeSerializers(all_exchanges, many=True)
        return JsonResponse(serializers.data, status=200, safe=False)
    if request.method == 'POST':
        serializers = ExchangeSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201, safe=True)
        else:
            if person_id:
                exchange = Exchange.objects.create(
                    person=person,
                    amount=amount,
                    exchange_type='D',
                    status='F'
                )
            return JsonResponse(serializers.error, status=400, safe=True)


# ####### collaborations section #######
def ask_for_collaboration(request, from_fact_id, to_fact_id):
    asker_collab = get_object_or_404(Factor, id=from_fact_id)
    interested_fac = get_object_or_404(Factor, id=to_fact_id)
    interested_fac.collab_guest.add(asker_collab)
    interested_fac.save()
    serializers = FactorSerializer(interested_fac)
    return JsonResponse(serializers.data, status=200, safe=False)


def accept_a_collaboration(request, asker_fact_id, factor_id):
    asker_factory = get_object_or_404(Factor, id=asker_fact_id)
    factor = get_object_or_404(Factor, id=factor_id)
    factor.collab_guest.remove(asker_factory)
    factor.collaborators.add(asker_factory)
    factor.save()
    serializers = FactorSerializer(factor)
    return JsonResponse(serializers.data, status=200, safe=False)



class GetAllCollaborationsFactorAPIView(APIView):
    def get(self, request, factor_pk):
        factor = get_object_or_404(Factor, pk=factor_pk)
        all_collaborations = factor.collaborations.order_by('-collab_date')
        serializers = CollaborationSerializer(all_collaborations, many=True)
        return Response(serializers.data, status=HTTP_200_OK)


class GetOneCommonCollaborationAPIView(APIView):
    def get(self, request, owner_id, asker_id):
        owner_factory = get_object_or_404(Factor, pk=owner_id)
        asker_factory = get_object_or_404(Factor, pk=asker_id)
        collaboration = Collaboration.objects.get(Q(factor=owner_factory) and Q(factor=asker_factory))
        serializers = CollaborationSerializer(collaboration)
        return Response(serializers.data, status=HTTP_200_OK)


class GetCollabOwnerAPIView(APIView):
    def get(self, request, collab_pk):
        collaboration = get_object_or_404(Collaboration, pk=collab_pk)
        for fac in collaboration.factor_set.filter():
            if collaboration.factor_asker == fac:
                pass
            else:
                serializers = FactorSerializer(fac)
                return Response(serializers.data, status=HTTP_200_OK)



class GetOrAddCollabItemAPIView(APIView):
    def get(self, request, collaboration_pk, item_pk):
        collaboration = get_object_or_404(Collaboration, pk=collaboration_pk)
        collab_item = collaboration.collab_items.get_or_create(item__id=item_pk)
        factor_asker = collaboration.factor_asker
        if collab_item[1]:
            collab_item.save()
            factor_asker.items_collaboration.add(collab_item.item)
            factor_asker.save()
            serializers = CollabItemSerializer(collab_item)
            return Response(serializers.data, status=HTTP_200_OK)
        return Response({'':''}, status=HTTP_400_BAD_REQUEST)



# ####### notifications section #######
def get_all_person_notifications(request, person_id):
    person = Person.objects.get(id=person_id)
    if  person.factor_set.first():
        factor = person.factor_set.first()
        notifications = Notification.objects.filter(Q(all_person_notifications=person) | Q(notifications_person_not_opened=person) | Q(all_factor_notifications=factor) | Q(notifications_factor_not_opened=factor)).order_by('-pub_date')
        serializers = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializers.data, status=200, safe=False)
    notifications = Notification.objects.filter(Q(all_person_notifications=person) | Q(notifications_person_not_opened=person)).order_by('-pub_date')
    serializers = NotificationSerializer(notifications, many=True)
    # print(notifications)
    return JsonResponse(serializers.data, status=200, safe=False)


def get_person_notifications(request, person_id):
    person = Person.objects.get(id=person_id)
    if  person.factor_set.first():
        factor = person.factor_set.first()
        notifications = Notification.objects.filter(Q(all_person_notifications=person) | Q(all_factor_notifications=factor)).order_by('-pub_date')
        serializers = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializers.data, status=200, safe=False)
    notifications = Notification.objects.filter(all_person_notifications=person).order_by('-pub_date')
    serializers = NotificationSerializer(notifications, many=True)
    # print(notifications)
    return JsonResponse(serializers.data, status=200, safe=False)


def get_person_not_opened_notifications(request, person_id):
    person = Person.objects.get(id=person_id)
    if  person.factor_set.first():
        factor = person.factor_set.first()
        notifications = Notification.objects.filter(Q(notifications_person_not_opened=person) | Q(notifications_factor_not_opened=factor)).order_by('-pub_date')
        serializers = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializers.data, status=200, safe=False)
    notifications = Notification.objects.filter(notifications_person_not_opened=person).order_by('-pub_date')
    serializers = NotificationSerializer(notifications, many=True)
    return JsonResponse(serializers.data, status=200, safe=False)


def open_person_notification(request, notification_id, person_id):
    person = get_object_or_404(Person, id=person_id)
    notification = get_object_or_404(Notification, id=notification_id)
    person.notifications_not_opened.remove(notification)
    person.notifications.add(notification)
    serializers = NotificationSerializer(notification)
    return JsonResponse(serializers.data, status=200, safe=False)


def open_factor_notification(request, notification_id, factor_id):
    factor = get_object_or_404(Person, id=factor_id)
    notification = get_object_or_404(Notification, id=notification_id)
    factor.notifications_not_opened.remove(notification)
    factor.notifications.add(notification)
    serializers = NotificationSerializer(notification)
    return JsonResponse(serializers.data, status=200, safe=False)



# ####### tries section #######
class TryModeViewSet(ModelViewSet):
    serializer_class = TrySerializer
    queryset = Try.objects.all()


@csrf_exempt
def add_try(request):
    if request.method == 'POST':
        serializers = TrySerializer(data=request.data)
        print(serializers.data)
        if serializers.is_valid():
            print(f"{serializer.data} is ok")
