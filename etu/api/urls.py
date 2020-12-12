from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
import os
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

router = routers.SimpleRouter()
router.register(r'items', ItemViewSet)
router.register(r'items_to_buy', ItemToBuyViewSet)
router.register(r'conditions', ConditionViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'users', UserViewSet)
router.register(r'item_types', TypeViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'purchased_items', PurchasedItemViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'bags', BagViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'feedbacks', FeedbackViewSet)

#LostItemsNameViewSet

urlpatterns = [
    url(r'^', include(router.urls)),
    path("fill_document/", views.fill_document, name="fill_document"),
    path("set_status/", views.set_status, name="set_status"),
    path("test/", views.test, name="test"),
    path("get_coords/", views.get_coords, name="get_coords"),
    path("test_file/", views.test_file, name="test_file"),
    #path('<str:filepath>/', views.download_file)
]

urlpatterns = format_suffix_patterns(urlpatterns)



    