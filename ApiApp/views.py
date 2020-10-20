from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import login as django_login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from ApiApp import admin
from BodegaApp.models import *
from ApiApp.serializers import *
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
####################
from django.db.models import Avg, Max, Min, Sum
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

#### PRUEBA DE LOGIN#####

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    # authorization_classes = [TokenAuthentication]
    # Detail define si es una petición de detalle o no, en methods añadimos el método permitido, en nuestro caso solo vamos a permitir post
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserSerializer(user).data,
            'access_token': token
        }
        if UserApp.objects.filter(pk=user.pk).get().image:
            image = UserApp.objects.filter(pk=user.pk).get().image
        return Response(data, status=status.HTTP_201_CREATED )


   # Todos los Provincias
class ProvinciaAllViewSet(viewsets.ModelViewSet):
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Provincia.objects.all()
        return queryset



    # Todos los municipios
class MunicipioAllViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        uui_prov = self.request.query_params.get('uiid')
        if uui_prov == None:
            queryset = Municipio.objects.all()
        else:
            queryset = Municipio.objects.filter(provincia__uui=uui_prov).all()
        return queryset


######BODEGA-- Todos los productos
# Aki se supone que cuando el ponga en la apk el id del admin(user, creo q des esta forma estoy usando el user del request, que es como el lo kiere) obtenga todos los productos de esa bodega

class BodegaAllProductosViewSet(viewsets.ModelViewSet):
    serializer_class = BodegaProductosSerializer
    # permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        userId = self.request.query_params.get('userid')
        queryset = ''
        if userId:
            queryset = Bodega.objects.filter(user__id=int(userId)).all()
        return queryset


   # Todos los Notificaciones
class NotificacionAllViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Notificacion_general.objects.all()
        return queryset

