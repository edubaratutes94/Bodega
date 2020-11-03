import base64
from django.core import exceptions
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator


from BodegaApp.models import *
from BodegaApp.utils import *

### PUEBA DE LOGIN @####

class UserLoginSerializer(serializers.Serializer):

    # Campos que vamos a requerir
    user = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['user'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')
        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class ActivatedUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activationCode = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


    class Meta:
        model = User
        fields = ('id', 'username', 'password')


# PROVINCIA
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('uui', 'nombre')


# MUNICIPIO
class MunicipioSerializer(serializers.ModelSerializer):
    provincia = serializers.SerializerMethodField()
    class Meta:
        model = Municipio
        fields = ('uui', 'nombre', 'provincia')

    def get_provincia(self, obj):
        return obj.provincia.uui


# bodega, devuelve por el user todos los productos de la bodega
class BodegaProductosSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Bodega
        fields = "__all__"

    def get_productos(self, obj):
        array = []
        for p in Producto.objects.filter(bodega__uui=obj.uii).all():
            dict = {}
            dict["uui"] = p.uui
            dict["nombre"] = p.nombre
            array.append(dict)
        return array


# Notificacion General
class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion_general
        fields = "__all__"

