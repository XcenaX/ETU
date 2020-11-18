
from api.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as Auth_User
import secrets

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["id", "name", "item_type", "condition", "address", "order_date", "receive_date", "provider", "price", "count", "weight"]
    
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        try:
            item = Item.objects.get(id=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def retrieve(self, request, pk=None):
        queryset = Type.objects.all()
        try:
            item_type = Type.objects.get(id=pk)
            serializer = TypeSerializer(item_type)
            return Response(serializer.data)
        except:
            raise Http404

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def retrieve(self, request, pk=None):
        queryset = Address.objects.all()
        try:
            address = Address.objects.get(id=pk)
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except:
            raise Http404

class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["id", "email", "role"]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            raise Http404

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    def retrieve(self, request, pk=None):
        queryset = Provider.objects.all()
        try:
            provider = Provider.objects.get(id=pk)
            serializer = ProviderSerializer(provider)
            return Response(serializer.data)
        except:
            raise Http404

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

    def retrieve(self, request, pk=None):
        queryset = Condition.objects.all()
        try:
            condition = Condition.objects.get(id=pk)
            serializer = ConditionSerializer(condition)
            return Response(serializer.data)
        except:
            raise Http404

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def retrieve(self, request, pk=None):
        queryset = Role.objects.all()
        try:
            role = Role.objects.get(id=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        except:
            raise Http404
