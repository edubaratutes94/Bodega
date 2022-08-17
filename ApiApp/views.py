from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ApiApp.serializers import *
from django.contrib.auth import login as django_login
from BodegaApp.utils import register_logs


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        register_logs(request, UserApp, "", user.__str__(), 10)
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"key": token.key, "userid": user.id}, status=200)

class ProductosBodega(viewsets.ModelViewSet):
    serializer_class = BodegaProductosSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = ''
        if self.request.user.id:
            queryset = Bodega.objects.filter(admin__id=self.request.user.id).all()
        return queryset

#NOMENCLADORES Listado-------------------------------------------------------------------------------

class UnidadMedidaList(viewsets.ModelViewSet):
    serializer_class = UnidadMedidaSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        return UnidadMedida.objects.all()

class ClasificacionList(viewsets.ModelViewSet):
    serializer_class = ClasificacionSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        return Clasificacion.objects.all()

class TipoOperacionList(viewsets.ModelViewSet):
    serializer_class = TipoOperacionSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        return TipoOperacion.objects.all()

class SeccionOperacionList(viewsets.ModelViewSet):
    serializer_class = SeccionOperacionSerializer
    permission_classes = [IsAuthenticated]
    authorization_classes = [TokenAuthentication]

    def get_queryset(self):
        return SeccionOperacion.objects.all()
#--------------------------------------------------------------------------------------------