from .models import *
from rest_framework import serializers
from django.core.serializers import serialize
from django.core.files.base import ContentFile
import base64
import six
import uuid
from .modules.hashutils import make_pw_hash
from django.http import Http404, JsonResponse
#import json



class RoleField(serializers.RelatedField):
    queryset = Role.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Role.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Role
        fields = ("id", "name")

class UserSerializer(serializers.ModelSerializer):
    role = RoleField(many=False, read_only=False)
    class Meta:
        model = User
        fields = ("id", "email", "password", "role")
    
    def create(self, validated_data):
        try:
            user = User.objects.filter(email=validated_data["email"]).first()
            if user:
                raise Exception
            
        except:
            raise serializers.ValidationError("User alredy exist")
        user = User.objects.create(
            role=validated_data['role'],
            email=validated_data['email'],
            password = make_pw_hash(validated_data['password'])
        )
        #user.password = validated_data['password']
        user.save()
        if user.role.name == "purchasing department admin":
            bag = Bag.objects.create(owner=user)
            bag.save()
        return user

class AddressField(serializers.RelatedField):
    queryset = Address.objects.all()
    def to_representation(self, value):
        address = Address.objects.get(id=value.id)
        return serialize("json", [address])
    def to_internal_value(self, data):
        try:
            try:
                return Address.objects.get(id=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class AddressSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Address
        fields = ("id", "name", "latitude", "longitude")
    

class TypeField(serializers.RelatedField):    
    queryset = Type.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        print(data)
        try:
            try:
                return Type.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )


class TypeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Type
        fields = ("id", "name")

class ProviderField(serializers.RelatedField):    
    queryset = Provider.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Provider.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class DatabaseConnectionField(serializers.RelatedField):    
    queryset = DatabaseConnection.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return DatabaseConnection.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class DatabaseConnectionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DatabaseConnection
        fields = [ "id", "host", "port", "database_name", "user", "password"]

class ProviderSerializer(serializers.ModelSerializer):    
    database_info = DatabaseConnectionField(many=False, read_only=False)
    class Meta:
        model = Provider
        fields = ("id", "name", "database_info")
        

class ConditionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Condition
        fields = ("id", "name")

class ConditionField(serializers.RelatedField):    
    queryset = Condition.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return Condition.objects.get(name=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )


class ItemSerializer(serializers.ModelSerializer):    
    provider = ProviderField(many=False, read_only=False)
    item_type = TypeField(many=False, read_only=False)
    class Meta:
        model = Item
        fields = ["id", "name", "item_type", "receive_date", "rfid", "provider", "price", "count", "image"]

class ItemField(serializers.RelatedField):    
    queryset = Item.objects.all()
    def to_representation(self, value):
        item = Item.objects.get(id=value.id)
        return serialize("json", [item])
    def to_internal_value(self, data):
        try:
            try:
                return Item.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class ItemToBuyField(serializers.RelatedField):    
    queryset = ItemToBuy.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return ItemToBuy.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class UserField(serializers.RelatedField):    
    queryset = User.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return User.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )


class DocumentSerializer(serializers.ModelSerializer):    
    condition = ConditionField(many=False, read_only=False)
    class Meta:
        model = Document
        fields = ["id", "condition", "date", "image"]


class DocumentField(serializers.RelatedField):    
    queryset = Document.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Document.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )


class PurchasedItemSerializer(serializers.ModelSerializer):    
    item = ItemToBuyField(many=False, read_only=False)
    user = UserField(many=False, read_only=False)
    document = DocumentField(many=False, read_only=False, required=False)
    class Meta:
        model = Purchased_Item
        fields = ["id", "item", "user", "document", "count", "status"]

    def create(self, validated_data):
        new_document = Document.objects.create()
        new_document.save()
        item = Purchased_Item.objects.create(
            user=validated_data['user'],
            count = validated_data['count'],
            item = validated_data['item'],
            document=new_document
        )
        
        item.save()
        return item

class PurchasedItemField(serializers.RelatedField):    
    queryset = Purchased_Item.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Purchased_Item.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )


class PurchaseSerializer(serializers.ModelSerializer):    
    purchased_items = PurchasedItemField(many=True, read_only=False, required=False)
    owner = UserField(many=False, read_only=False)
    class Meta:
        model = Purchase
        fields = ["id", "purchase_start_date", "purchase_end_date", "owner", "purchased_items"]

    def create(self, validated_data):
        item = Purchase.objects.create(
            owner=validated_data['owner'],
        )

        for element in validated_data["purchased_items"]:
            item.purchased_items.add(element)
        
        
        item.save()
        return item


class BagSerializer(serializers.ModelSerializer):    
    items = PurchasedItemSerializer(many=True, read_only=False)
    owner = UserSerializer(many=False, read_only=False)
    class Meta:
        model = Bag
        fields = [ "items", "owner"]


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = [ "id", "phone", "car_number", "fullname", "latitude", "longitude", "company_name"]


class DriverField(serializers.RelatedField):    
    queryset = Driver.objects.all()
    def to_representation(self, value):
        driver =  Driver.objects.get(id=value.id)
        return serialize( "json", [driver] )
    def to_internal_value(self, data):
        try:
            try:
                return Driver.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class OrderStatusField(serializers.RelatedField):    
    queryset = OrderStatus.objects.all()
    def to_representation(self, value):
        return value.name
    def to_internal_value(self, data):
        try:
            try:
                return OrderStatus.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class OrderStatusSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderStatus
        fields = [ "id", "name"]

class OrderSerializer(serializers.ModelSerializer):    
    item = ItemField(many=False, read_only=False, required=False)
    driver =  DriverField(many=False, read_only=False, required=False)
    address = AddressField(many=False, read_only=False, required=False)
    status = OrderStatusField(many=False, read_only=False, required=False)
    class Meta:
        model = Order
        fields = [ "id", "item", "status", "driver",  "city", "address", "count"]

class OrderField(serializers.RelatedField):    
    queryset = Order.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return Order.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Type.DoesNotExist:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )



class ItemToBuySerializer(serializers.ModelSerializer):    
    provider = ProviderField(many=False, read_only=False)
    item_type = TypeField(many=False, read_only=False)
    class Meta:
        model = ItemToBuy
        fields = ["id", "name", "item_type", "provider", "price", "image", "url_name"]

class FeedbackSerializer(serializers.ModelSerializer):
    order = OrderField(many=False, read_only=False)
    class Meta:
        model = Feedback
        fields = [ "id", "image", "message", "order"]
