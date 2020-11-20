
from api.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, JsonResponse
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
from django.shortcuts import render

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib.styles import ParagraphStyle

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django.views.decorators.csrf import csrf_exempt

from etu.settings import BASE_DIR

import mimetypes

from django.http import HttpResponse, FileResponse

class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "item_type", "address", "order_date", "receive_date", "provider", "price", "count", "weight"]
    
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
    filter_fields = ["email", "role"]

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

class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "item_type", "address", "order_date", "receive_date", "provider", "price", "count", "weight"]
    
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

class DocumentViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["condition"]
    
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def retrieve(self, request, pk=None):
        queryset = Document.objects.all()
        try:
            item = Document.objects.get(id=pk)
            serializer = DocumentSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class PurchasedItemViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["user"]
    
    queryset = Purchased_Item.objects.all()
    serializer_class = PurchasedItemSerializer

    def retrieve(self, request, pk=None):
        queryset = Purchased_Item.objects.all()
        try:
            item = Purchased_Item.objects.get(id=pk)
            serializer = PurchasedItemSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404


class PurchaseViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["owner"]
    
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def retrieve(self, request, pk=None):
        queryset = Purchase.objects.all()
        try:
            item = Purchase.objects.get(id=pk)
            serializer = PurchaseSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404


class BagViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["owner"]
    
    queryset = Bag.objects.all()
    serializer_class = BagSerializer

    def retrieve(self, request, pk=None):
        queryset = Bag.objects.all()
        try:
            item = Bag.objects.get(id=pk)
            serializer = BagSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

def download_file(request):
    fl_path = '/file/path'
    filename = 'downloaded_file_name.extension'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

@csrf_exempt
def fill_document(request):
    if request.method == "POST":
        item_id = request.POST["id"]
        if not item_id: 
            return JsonResponse({"error": "Parameter id is required!"})
        item = Purchased_Item.objects.filter(id=item_id).first()
        if not item:
            error = "Item with id=" + item_id + " not found!"
            return JsonResponse({"error": error})
        
        fl_path = BASE_DIR + "/media/dogovors/"
        
        pdfmetrics.registerFont(TTFont('cmunss', 'media/fonts/cmunss.ttf'))
        packet = io.BytesIO()

        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('cmunss', 12)
        can.drawString(45, 585, item.item.provider.name)
        can.drawString(90, 260, str(item.get_total_price()) + "тг")
        can.drawString(130, 178, item.item.name)
        can.drawString(85, 158, str(item.count) + " едениц")

        can.save()
        can.showPage()
        #packet.seek(0)
        new_pdf = PdfFileReader(packet)

        existing_pdf = PdfFileReader(open("media/dogovor.pdf", "rb"))
        output = PdfFileWriter()

        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

        document_path = "media/dogovors/" + str(item.id) + ".pdf"
        absolute_path = BASE_DIR + "//media//dogovors//" + str(item.id) + ".pdf"
        
        filename = str(item.id) + ".pdf"

        outputStream = open(document_path, "wb")
        output.write(outputStream)
        outputStream.close()

        item.document.image = document_path
        item.document.save()
        return FileResponse(open(absolute_path, 'rb'), content_type='application/pdf')
    return JsonResponse({"error": "Only POST method is allowed!"})

def test(request):
    return render(request, "test.html", {})