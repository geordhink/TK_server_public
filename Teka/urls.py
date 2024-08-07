from django.urls import path, include
from .models import *
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import re_path
import json


router = DefaultRouter()
router.register('persons', PersonsViewSet, basename='persons')
router.register('persons-update', PersonUpdateViewSet, basename='persons-update')
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
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('collaborations', CollaborationViewSet, basename='collaborations')
router.register('collab_items', CollabItemViewSet, basename='collab_items')
router.register('comments', CommentViewSet, basename='comments')
# router.register('person-pic', ChangePersonImageViewSets, basename='person-pic')
# router.register('factor-pic', ChangePersonImageViewSets, basename='factor-pic')
# particulary
# router.register('get_one_common_collab', GetOneCommonCollaborationViewset, basename='get_one_common_collab')

app_name = 'Teka'

urlpatterns = [
    # ####### globals section #######
    path('', global_view),
    path('change_picture/<int:person_id>/<int:factor_id>/', change_picture, name='change_picture'),
    # ####### globals viewsets section ####glo###
    path('viewsets/', include(router.urls), name="viewsets"),
    path('viewsets/<int:pk>/', include(router.urls), name="viewsets"),
    # ####### registration and login section #######
    path('register/', RegisterUser.as_view()),
    # ####### socials networks section #######
    re_path(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    # ####### person section #######
    path('get_login_by_token/<str:key>/', GetLoginByToken.as_view()),
    path('get_person_by_user_id/<int:user_id>/', GetPersonByUserId.as_view()),
    path('change_person_favorite_currency/<int:person_id>/<str:currency>/', change_person_favorite_currency),
    path('get_one_person_by_client_id/<int:client_id>/', GetOnePersonByClientId.as_view()),
    # ####### markets section #######
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
    path('retrieve_factors_search/<str:searched_text>/', RetrieveFactorSearch.as_view()),
    path('retrieve_items_searched/<str:searched_text>/', RetrieveItemsSearched.as_view()),
    path('retrieve_items_searched_typed/<str:searched_text>/<str:item_type>/', RetrieveItemsSearchedTyped.as_view()),
    path('retrieve_all_factor_items_search/<str:searched_text>/<int:factor_pk>/', RetrieveAllFactorItemsSearched.as_view()),
    path('retrieve_specials_transactions_searched/<str:searched_text>/', RetrieveSpecialsTransactionsSearched.as_view()),
    path('create_or_update_client_transaction_by_item/<int:person_id>/<int:item_id>/<int:quantity>/', UpdateOrCreateClientTransactionByItem.as_view()),
    path('remove_one_transaction_of_client/<int:client_id>/<int:item_id>/', remove_one_transaction_of_client),
    path('remove_all_transaction_of_client/<int:client_id>/', remove_all_transaction_of_client),
    path('get_person_s_factory/<int:person_id>/', get_person_s_factory),
    path('get_item_factor/<int:item_id>/', get_item_factor),
    path('create_then_add_item_in_factor/<int:factor_id>/', CreateThenAddItemInFactor.as_view()),
    path('update_item_in_factor/<int:factor_id>/', UpdateItemInFactorAPIView.as_view()),
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
    path('register_new_factor/', RegisterNewFactor.as_view()),
    path('list_all_factors_with_items/', list_all_factors_with_items),
    path('list_all_typed_items/<str:item_type>/', GetAllTypeSpecifiedItems.as_view()),
    path('get_factor_best_clients/<int:factor_id>/', get_factor_best_clients),
    path('get_factor_best_clients/<int:factor_id>/<int:nb>/', get_factor_best_clients),
    # ####### collaborations section #######
    path('ask_for_collaboration/<int:from_fact_id>/<int:to_fact_id>/', ask_for_collaboration),
    path('cancel_the_collaboration/<int:from_fact_id>/<int:to_fact_id>/', cancel_the_collaboration),
    path('accept_a_collaboration/<int:asker_fact_id>/<int:factor_id>/', accept_a_collaboration),
    path('get_all_collaborations_factor/<int:factor_pk>/', GetAllCollaborationsFactorAPIView.as_view()),
    path('get_collab_owner/<int:collab_pk>/', GetCollabOwnerAPIView.as_view()),
    path('list_all_collab_distributors/<int:factor_pk>/', ListAllCollabDistributorsFactor.as_view()),
    path('list_all_collab_sellers/<int:factor_pk>/', ListAllCollabSellersFactor.as_view()),
    path('get_one_common_collab/<int:owner_id>/<int:asker_id>/', GetOneCommonCollaborationAPIView.as_view(),),
    path('get_or_add_collab_item/<int:collaboration_pk>/<int:item_pk>/', GetOrAddCollabItemAPIView.as_view(),),
    path('list_suggested_collaborators/<int:factor_pk>/', CollaborationSuggestApiView.as_view(),),
    # ####### notifications section #######
    path('get_all_person_notifications/<int:person_id>/', get_all_person_notifications),
    path('get_person_notifications/<int:person_id>/', get_person_notifications),
    path('get_person_not_opened_notifications/<int:person_id>/', get_person_not_opened_notifications),
    path('open_person_notification/<int:notification_id>/<int:person_id>/', open_person_notification),
    path('open_person_all_not_view_notifications/<int:person_id>/', open_person_all_not_view_notifications),
    path('open_factor_notification/<int:notification_id>/<int:factor_id>/', open_factor_notification),
    # ####### Comments section #######
    path('get_all_item_comments/<int:item_pk>/', GetAllItemCommentsAPIView.as_view()),
    path('post_item_comment/<int:item_pk>/<int:person_pk>/', PostItemComment.as_view()),

    # ####### tries section #######
    path("add_try/", add_try),

]
