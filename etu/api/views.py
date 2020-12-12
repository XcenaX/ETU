
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
from django.core.files import File
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from etu.settings import BASE_DIR

from urllib.request import urlopen

import requests

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django.views.decorators.csrf import csrf_exempt

from tempfile import NamedTemporaryFile
import mimetypes

from django.http import HttpResponse, FileResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

from datetime import datetime
API_KEY = "AIzaSyCcHCB9lx35nurrIOy2KvphPIvmsflB4mE"

import googlemaps

import sqlite3
import shutil
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ItemViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "item_type",  "receive_date", "provider", "price", "count"]
    authentication_classes = [CsrfExemptSessionAuthentication]
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


class ItemToBuyViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "item_type", "provider", "price"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = ItemToBuy.objects.all()
    serializer_class = ItemToBuySerializer

    def retrieve(self, request, pk=None):
        queryset = ItemToBuy.objects.all()
        try:
            item = ItemToBuy.objects.get(id=pk)
            serializer = ItemToBuySerializer(item)
            return Response(serializer.data)
        except:
            raise Http404


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    filter_fields = ["name", "item_type", "receive_date", "rfid", "provider", "price", "count"]
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    filter_fields = ["user", "status"]
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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
    authentication_classes = [CsrfExemptSessionAuthentication]
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

class DriverViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["fullname", "phone", "car_number"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def retrieve(self, request, pk=None):
        queryset = Driver.objects.all()
        try:
            item = Driver.objects.get(id=pk)
            serializer = DriverSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class OrderViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["status", "count"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        try:
            item = Order.objects.get(id=pk)
            serializer = OrderSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

class FeedbackViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["message"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def retrieve(self, request, pk=None):
        queryset = Feedback.objects.all()
        try:
            item = Feedback.objects.get(id=pk)
            serializer = FeedbackSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

@csrf_exempt
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
        
        font = ImageFont.truetype( BASE_DIR + '//media//fonts//cmunss.ttf', 35)

        img = Image.open(BASE_DIR + "//media//dogovor.jpg").convert("RGB")

        draw = ImageDraw.Draw(img)
        draw.text((135, 415), item.item.provider.name, (0,0,0), font=font)
        draw.text((254, 1307), str(item.get_total_price()) + "тг", (0,0,0), font=font)
        draw.text((374, 1535), item.item.name, (0,0,0), font=font)
        draw.text((234, 1595), str(item.count) + " едениц", (0,0,0), font=font)

        absolute_path = BASE_DIR + "//media//dogovors//" + str(item.id) + ".jpg"
        img.save(absolute_path)

        document_path = "media/dogovors/" + str(item.id) + ".pdf"

        item.document.image = document_path
        item.document.save()
        return FileResponse(open(absolute_path, 'rb'), content_type='application/png')
    return JsonResponse({"error": "Only POST method is allowed!"})

def test(request):
    return render(request, "test.html", {})

@csrf_exempt
def set_status(request):
    if request.method == "POST":
        item_to_buy_id = request.POST["id"]
        
        if not item_to_buy_id:
            return JsonResponse({"error": "id parameter required!"})
        item = Purchased_Item.objects.filter(id=item_to_buy_id).first()
        
        if not item:
            return JsonResponse("Item with id not found!")
        if item.status is True:
            return JsonResponse({"error": "This item is already delivered!"})
        item.status = True
        item.save()

        new_item = Item.objects.create(name=item.item.name, item_type=item.item.item_type, receive_date=datetime.now(), provider=item.item.provider, price=item.item.price, count=item.count, image=item.item.image)
        new_item.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def get_coords(request):
    if request.method == "POST":
        name = ""
        try:
            name = request.POST["name"]
            data = requests.post("https://maps.googleapis.com/maps/api/geocode/json?address=" + name + "&key="+API_KEY)
            
            if data.json()["status"] == "ZERO_RESULTS":
                return JsonResponse({"error": "Not found!"})
            
            return JsonResponse({
                "longitude": data.json()["results"][0]["geometry"]["location"]["lng"],
                "latitude": data.json()["results"][0]["geometry"]["location"]["lat"]
                })
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)})

    return JsonResponse({"error": request.method + " method not allowed!"})


def check_table_names(names):
    my_table_names = ["name", "image", "price", "item_type", "provider"]
    for name in my_table_names:
        if name not in names:
            return False
    return True  

@csrf_exempt
def test_file(request):
    if request.method == "POST":
        name = ""
        
        file = request.FILES["file"]

        db_file = open("temp_db", "wb")
        
        for chunk in file.chunks():
                db_file.write(chunk)
        
        if file.name.endswith(".sqlite3") or file.name.endswith(".sqlite") or file.name.endswith(".db") or file.name.endswith(".sql"):
            conn = None
            
            try:
                conn = sqlite3.connect(db_file.name)
                cursor = conn.cursor()

                cursor.execute("select * from items;")
                rows = cursor.fetchall()
                table_names = list(map(lambda x: x[0], cursor.description))
                if not check_table_names(table_names):
                    return JsonResponse({"error": "Your database file does not match the type of our database!"})
                
                for row in rows:
                    provider = Provider.objects.create(name=row[4])
                    item_type = Type.objects.create(name=row[5])
                    item = ItemToBuy.objects.create(name=row[1], price=row[3], provider=provider, item_type=item_type)
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(row[2]).read())
                    img_temp.flush()
                    item.image.save(f"image_{item.id}.png", File(img_temp))
                    item.save()
            except Exception as e:
                return JsonResponse({
                    "error": str(e),
                })
                print(e)
            finally:
                if conn:
                    conn.close()


            return JsonResponse({"names": table_names})
        elif file.name.endswith(".sql"):
            print("test")
        elif file.name.endswith(".ns"):
            print("test")

        
        
        
        
        return JsonResponse({
            "success": True,
        })
        

    return JsonResponse({"error": request.method + " method not allowed!"})