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
# from BodegaApp import models, forms
from BodegaApp.models import *
from ApiApp.serializer import *

class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # passw = serializer.validated_data["password"]
        # register_logs(request, UserApp, "", user.__str__(), 10)
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        # token1, created1 = Token.objects.get_or_create(password=passw)
        image = None
        if UserApp.objects.filter(pk=user.pk).get().image:
            image = UserApp.objects.filter(pk=user.pk).get().image

        return Response({ "token": token.key, "username": request.user.username,
                         "avatar": image.url if image != None else None, "userid": user.id}, status=200)



# Todas las provincias
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

