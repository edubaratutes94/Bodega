import datetime
import uuid
import os
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.conf import settings
from django.db.models.signals import *
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
class UserApp(User):
    uui = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    image = models.ImageField(upload_to='static/users', verbose_name="Avatar",
                              null=True, default='static/users/userDefault1.png')
    referUser = models.UUIDField(null=True)
    fa2 = models.BooleanField(verbose_name="2FA", default=False)

    def __str__(self):
        return str(self.username)

    def Online(self):
        for s in Session.objects.all():
            if s.get_decoded():
                if self.id == int(s.get_decoded()['_auth_user_id']):
                    now = datetime.datetime.now()
                    dif = (now - s.expire_date)
                    if dif < datetime.timedelta(seconds=0):
                        return True
        return False

    class Meta:
        verbose_name_plural = "Usuarios"


class Provincia(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Provincias"

# NOMENCLADOR MUNICIPIO
class Municipio(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    provincia = models.ForeignKey(Provincia, verbose_name="Provincia", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Municipios"

class ConsejoPopular(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    municipio = models.ForeignKey(Municipio, verbose_name="Municipio", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Consejos Populares"


class Zona(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    consejo = models.ForeignKey(ConsejoPopular, verbose_name="Consejo Popular", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)+ "  --  " + self.consejo.nombre

    class Meta:
        verbose_name_plural = "Zonas"

class Clasificacion(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Clasificaciones"

class UnidadMedida(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Unidad de Medida", unique=True)
    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Unidades de Medidas"


class Producto(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=100, verbose_name="Código", null=True)
    precio_venta = models.FloatField(verbose_name="Precio de Venta")
    precio_costo = models.FloatField(verbose_name="Precio de Costo")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    unidad = models.ForeignKey(UnidadMedida, verbose_name="Unidad de Medidas", on_delete=models.CASCADE)
    clasificacion = models.ForeignKey(Clasificacion, verbose_name="Clasificación", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Productos"


class Bodega(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    admin = models.ForeignKey(User, verbose_name="Administrador", on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, verbose_name="Zona", on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto,verbose_name="Productos")

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Bodegas"

class TipoOperacion(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Operaciones"

class Notificacion_general(models.Model):
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=100, verbose_name="Título")
    fecha = models.DateTimeField( verbose_name="Fecha", auto_now=True)
    mensaje = models.TextField(max_length=250, verbose_name="Mensaje")

    def __str__(self):
        return str(self.titulo)

    class Meta:
        verbose_name_plural = "Notificaciones"


# class SeccionOperacion(models.Model):
#     nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
#
#     def __str__(self):
#         return str(self.nombre)
#
#     class Meta:
#         verbose_name_plural = "Sección de operaciones"
#
# class Operacion(models.Model):
#     fecha = models.DateTimeField(verbose_name="Fecha", auto_now=True)
#     cantidad = models.FloatField(verbose_name="Cantidad")
#     cantidad = models.FloatField(verbose_name="Cantidad")
#     cantidad = models.FloatField(verbose_name="Cantidad")
#     cantidad = models.FloatField(verbose_name="Cantidad")



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
