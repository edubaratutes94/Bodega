import base64
from django.core import exceptions
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from BodegaApp.models import *
from BodegaApp.utils import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # imei = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    userApp = UserApp.objects.filter(pk=user.pk).get()
                    data["user"] = user
                else:
                    msg = {"msg":"Usuario desactivado"}
                    print(msg)
                    raise exceptions.ValidationError(msg)
            else:
                user = User.objects.filter(username=username)
                if user.count() > 0:
                    if not user.get().is_active:
                        msg = {"msg": "500"} #usuario pendiente de activacion
                        print(msg)
                        raise exceptions.ValidationError(msg)
                    else:
                        msg = {"msg": "Error en el login, credenciales erroneas."}
                        print(msg)
                        raise exceptions.ValidationError(msg)
                else:
                    msg = {"msg":"Error en el login, credenciales erroneas."}
                    print(msg)
                    raise exceptions.ValidationError(msg)
        else:
            msg = {"msg":"Debe escribir usuario o contraseña, los dos!"}
            print(msg)
            raise exceptions.ValidationError(msg)
        return data

class ActivatedUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activationCode = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


# PROVINCIA
class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('uui', 'nombre')


# MUNICIPIO
class MunicipioSerializer(serializers.ModelSerializer):
    # provincia = serializers.SerializerMethodField()
    class Meta:
        model = Municipio
        fields = ('uui', 'nombre', 'provincia')
