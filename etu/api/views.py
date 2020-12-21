
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

import mysql.connector
from mysql.connector import Error
import shutil

from .modules.hashutils import check_pw_hash, make_pw_hash

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# for order in OrderStatus.objects.all():
#     order.delete()




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


class OrderStatusViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer

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
    filter_fields = ["status", "count", "driver"]
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


class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["host"]
    authentication_classes = [CsrfExemptSessionAuthentication]
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer

    def retrieve(self, request, pk=None):
        queryset = DatabaseConnection.objects.all()
        try:
            item = DatabaseConnection.objects.get(id=pk)
            serializer = DatabaseConnectionSerializer(item)
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

@csrf_exempt
def fill_waybill(request):
    if request.method == "POST":
        order_id = request.POST["id"]
        if not order_id: 
            return JsonResponse({"error": "Parameter id is required!"})
        order = Order.objects.filter(id=order_id).first()
        if not order:
            error = "Order with id=" + order_id + " not found!"
            return JsonResponse({"error": error})
        
        font = ImageFont.truetype( BASE_DIR + '//media//fonts//cmunss.ttf', 25)

        img = Image.open(BASE_DIR + "//media//nakladnaya.jpg").convert("RGB")

        draw = ImageDraw.Draw(img)
        draw.text((590, 125), str(order.id), (0,0,0), font=font)
        draw.text((50, 350), "1", (0,0,0), font=font)
        draw.text((120, 350), order.item.name, (0,0,0), font=font)
        draw.text((480, 350), str(order.count), (0,0,0), font=font)
        draw.text((570, 350), str(order.item.price) + " тг", (0,0,0), font=font)
        draw.text((700, 350), str(order.get_total_price()) + " тг", (0,0,0), font=font)
        draw.text((130, 165), order.client_name, (0,0,0), font=font)

        absolute_path = BASE_DIR + "//media//waybills//" + str(order.id) + ".jpg"
        img.save(absolute_path)

        document_path = "media/waybills/" + str(order.id) + ".pdf"
        if not order.document:
            order.document = Document.objects.create()
        order.document.image = document_path
        order.document.save()
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
def fill_database(request):
    if request.method == "POST":
        db_host = "remotemysql.com"
        port = "3306"
        db_name = "TIdx9NcJTR"
        user = "TIdx9NcJTR"
        password = "tnIbzSmeDV"
        provider_name = request.POST["provider"]
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(host=db_host, database=db_name, user=user, passwd=password, port=port)
            if connection.is_connected():
                sql_select_Query = "select * from items"
                cursor = connection.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                

                
                for row in records:
                    print("Id = ", row[0], )
                    print("Name = ", row[1])
                    print("Image = ", row[2])
                    print("Price  = ", row[3])
                    print("Item type  = ", row[4])
                    item_type = None
                    provider = None
                    if len(Type.objects.filter(name=row[4])) == 0:
                        Type.objects.create(name=row[4])
                    if len(Provider.objects.filter(name=provider_name)) == 0:
                        Provider.objects.create(name=provider_name)

                    item_type = Type.objects.filter(name=row[4]).first()
                    provider = Provider.objects.filter(name=provider_name).first()

                    item = ItemToBuy.objects.create(name=row[1], price=row[3], item_type=item_type, provider=provider)
                    
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(row[2]).read())
                    img_temp.flush()
                    item.image.save(f"image_{item.id}.png", File(img_temp))
                    item.save()

                    
                return JsonResponse({"success": item})

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection and cursor:
                cursor.close()
                connection.close()
                print("MySQL connection is closed")        
        return JsonResponse({
            "success": True,
        })

    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def register(request):
    if request.method == "POST":
        role_id = request.POST["role"]
        role = Role.objects.filter(id=role_id).first()
        email = request.POST["email"]
        password = request.POST["password"]
        company_name = request.POST["company"]

        if len(User.objects.filter(email=email)) > 0:
            return JsonResponse({"error": "User with this email already exist!"})
        user = User.objects.create(email=email, role=role, password=make_pw_hash(password), company_name=company_name)
        user.save()
        return JsonResponse({"success": True}) 

    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        users = User.objects.filter(email=email)
        if len(users) == 0:
            return JsonResponse({"error": "User with this email doesn't exist!"})
        user = users.first()
        print(password)
        print(user.password)
        if check_pw_hash(password, user.password):
            return JsonResponse({
                "success": True,
                "user":{
                    "id": user.id,
                    "email": user.email,
                    "role_id": user.role.id,
                    "role": user.role.name,
                },
            }) 
        return JsonResponse({"error": "Incorrect email or password!"})        
    return JsonResponse({"error": request.method + " method not allowed!"})


@csrf_exempt
def set_database_connection_info(request):
    if request.method == "POST":
        host = request.POST["host"]
        port = request.POST["port"]
        user = request.POST["user"]
        password = request.POST["password"]
        database_name = request.POST["database_name"]
        user_id = requests.POST["user_id"]
        user = User.objects.get(id=user_id)

        user.database_info = DatabaseConnection.objects.create(host=host, port=port, database_name=database_name, login=user, password=password)
        user.database_info.save()
        user.save()

        return JsonResponse({"success": True}) 

    return JsonResponse({"error": request.method + " method not allowed!"})
