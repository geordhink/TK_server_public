from django.urls import path, include
from .models import *
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import re_path


router = DefaultRouter()
router.register('persons', PersonsViewSet, basename='persons')
router.register('profils', ProfilViewSet, basename="profils")
router.register('medias', MediaViewSet, basename="medias")
router.register('items', ItemViewSet, basename="items")
router.register('transactions', TransactionViewSet, basename="transactions")
router.register('factors', FactorViewSet, basename="factors")
router.register('clients', ClientViewSet, basename="clients")
router.register('physical_items', GetPhysicalItems, basename="physical_items")
router.register('virtual_items', GetVirtualItems, basename="virtual_items")
router.register('tries', TryModeViewSet, basename="tries")
router.register('users', UserModelViewSet, basename='users')

app_name = 'Teka'

urlpatterns = [
    path('viewsets/', include(router.urls), name="viewsets"),
    path('viewsets/<int:pk>/', include(router.urls), name="viewsets"),
    # registration and login
    path('register/', RegisterUser.as_view()),
    # facebook urls
    re_path(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    # person
    path('get_login_by_token/<str:key>/', GetLoginByToken.as_view()),
    path('get_person_by_user_id/<int:user_id>/', GetPersonByUserId.as_view()),
    # market
    path('get_factor_by_person/<int:person_id>/', GetFactorByPerson.as_view()),
    path('get_client_by_person/<int:person_id>/', GetClientByPerson.as_view()),
    path('get_transaction_by_item/<int:item_id>/', GetTransactionByItem.as_view()),
    path('get_client_transactions/<int:client_id>/', GetClientTransactions.as_view()),
    path('get_or_create_client_person/<int:person_id>/', GetOrCreatePersonClient.as_view()),
    path('add_item_to_factor/<int:item_id>/<int:factor_id>/', AddItemToFactor.as_view()),
    path('get_all_factor_items/<int:factor_id>/', GetAllFactorItems.as_view()),
    path('client_buy_item_by_transaction/<int:client_id>/<int:item_id>/', ClientBuyItemByTransaction.as_view()),
    path('get_last_created_items/', GetLastCreatedItems.as_view()),
    path('global_search/<str:search_word>/', GlobalSearch.as_view()),
    path('retrieve_factor_items_search/<int:factor_id>/<str:searched_text>/', RetrieveFactorItemsSearch.as_view()),
    path('create_or_update_client_transaction_by_item/<int:person_id>/<int:item_id>/<int:quantity>/', UpdateOrCreateClientTransactionByItem.as_view()),
    path('remove_one_transaction_of_client/<int:client_id>/<int:item_id>/', remove_one_transaction_of_client),
    path('get_person_s_factory/<int:person_id>/', get_person_s_factory),
    path('get_item_factor/<int:item_id>/', get_item_factor),
    path('create_then_add_item_in_factor/<int:factor_id>/', CreateThenAddItemInFactor.as_view()),
    path('deposit_exchange/<int:person_id>/<int:amount>/', deposit_exchange),
    path('add_person_amount/<int:person_id>/<int:amount>/', add_person_amount),
    path('pay_cart_items/<int:client_id>/', PayCartItems.as_view()),
    path('retrieve_one_client_by_transaction/<int:factor_id>/<int:transaction_id>/', RetrieveOneClientByTransactionAPIView.as_view()),
    path('retrieve_all_items_bought_by_client/<int:client_id>/', RetrieveAllItemsBoughtByClientAPIView.as_view()),
    path('third_last_transactions_by_client/<int:client_id>/', ThirdLastTransactionsByClientAPIView.as_view()),
    path('third_last_transactions_by_factor/<int:factor_id>/', ThirdLastTransactionsByFactorAPIView.as_view()),
    path('third_last_transactions_factor_by_person/<int:person_id>/', ThirdLastTransactionsFactorClientByPersonAPIView.as_view()),
    path('retrieve_all_transactions_done_by_client/<int:client_id>/', RetrieveAllTransactionsDoneByClientAPIView.as_view()),
    path('retrieve_one_item_all_transactions_done/<int:item_id>/', RetrieveOneItemAllTransactionsDoneAPIView.as_view()),
    path('list_all_random_items_by_type/<str:type_str>/', ListAllRandomItemsByTypeAPIView.as_view()),
    path('get_flux_factors_transactions/<int:person_id>/<str:flux>/', get_flux_factors_transactions),
    path('get_flux_factors_transactions_status/<int:person_id>/<str:flux>/<str:status>/', get_flux_factors_transactions_status),
    path('follow_action_client_factor/<int:client_id>/<int:factor_id>/', follow_action_client_factor),
]
