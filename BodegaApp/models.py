import datetime
import uuid
import os
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models
from django.conf import settings
from django.db.models.signals import *
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

class UserApp(User):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    image = models.ImageField(upload_to='static/users', verbose_name="Avatar",
                              null=True, default='static/users/userDefault1.png')

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Provincias"

# NOMENCLADOR MUNICIPIO
class Municipio(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    provincia = models.ForeignKey(Provincia, verbose_name="Provincia", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Municipios"

class ConsejoPopular(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    municipio = models.ForeignKey(Municipio, verbose_name="Municipio", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Consejos Populares"


class Zona(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    consejo = models.ForeignKey(ConsejoPopular, verbose_name="Consejo Popular", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.nombre) + "  --  " + self.consejo.nombre

    class Meta:
        verbose_name_plural = "Zonas"

class Clasificacion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Clasificaciones"

class UnidadMedida(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Unidad de Medida", unique=True)
    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Unidades de Medidas"


class Producto(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=100, verbose_name="Código", null=True,  unique=True)
    precio_venta = models.FloatField(verbose_name="Precio de Venta",validators=[MinValueValidator(0)])
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    unidad = models.ForeignKey(UnidadMedida, verbose_name="Unidad de Medidas", on_delete=models.PROTECT)
    clasificacion = models.ForeignKey(Clasificacion, verbose_name="Clasificación", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Productos"


class Bodega(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    admin = models.ForeignKey(UserApp, verbose_name="Administrador", on_delete=models.PROTECT)
    zona = models.ForeignKey(Zona, verbose_name="Zona", on_delete=models.PROTECT, null=True)
    productos = models.ManyToManyField(Producto, verbose_name="Productos")

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Bodegas"



class TipoOperacion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Operaciones"


class ProdPrecioCosto(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.PROTECT, null=True)
    fecha = models.DateTimeField(verbose_name="Fecha", auto_now=True)
    valor = models.FloatField(verbose_name="Valor", default=0, blank=True, validators=[MinValueValidator(0)])
    def __str__(self):
        return str(self.producto.nombre)


class Notificacion_general(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=100, verbose_name="Título")
    fecha = models.DateTimeField( verbose_name="Fecha", auto_now=True)
    mensaje = models.TextField(max_length=250, verbose_name="Mensaje")

    def __str__(self):
        return str(self.titulo)

    class Meta:
        verbose_name_plural = "Notificaciones"


class SeccionOperacion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    tipo_operacion = models.ForeignKey(TipoOperacion, verbose_name="Tipo de Operación",
                                       on_delete=models.PROTECT)


    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Sección de operaciones"

class Operacion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    factura = models.CharField(max_length=100, verbose_name="Número de Factura", blank=True,
                               help_text="En caso de operación por Facturación")
    fecha = models.DateTimeField(verbose_name="Fecha", auto_now=True)
    cantidad = models.FloatField(verbose_name="Cantidad", default=0, blank=True, validators=[MinValueValidator(0)])
    imp_pv = models.FloatField(verbose_name="Imp/PV", default=0, blank=True, validators=[MinValueValidator(0)])
    imp_pc = models.FloatField(verbose_name="Imp/PC", default=0, blank=True, validators=[MinValueValidator(0)])
    # precio_costo = models.FloatField(verbose_name="Precio de Costo", null=True, validators=[MinValueValidator(0)])
    seccion_operacion = models.ForeignKey(SeccionOperacion, verbose_name="Sección de Operación",
                                          on_delete=models.CASCADE, null=True)
    bodega = models.ForeignKey(Bodega, verbose_name="Bodega", on_delete=models.PROTECT, null=True)
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.PROTECT, null=True)



    # @classmethod
    # def get_saldo_total(cls):
    #
    #     return sum([total.saldo_final for total in cls.objects.all()])


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

    for user in User.objects.all():
        Token.objects.get_or_create(user=user)

#Se agregan las nuevas tablas
class Traslado(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    bodega_origen = models.ForeignKey(Bodega, verbose_name="Bodega de Origen", on_delete=models.PROTECT, related_name="BodegaOrigen")
    bodega_destino = models.ForeignKey(Bodega, verbose_name="Bodega de Destino", on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.PROTECT)
    cantidad = models.FloatField(verbose_name="Cantidad")
    fecha_traslado = models.DateTimeField(verbose_name="Fecha de traslado")
    bodega_origen_confirmacion = models.BooleanField(verbose_name="Confirmacion Bodega Origen")
    bodega_destino_confirmacion = models.BooleanField(verbose_name="Confirmacion Bodega Destino")

    def __str__(self):
        return 'De ' + str(self.bodega_origen.nombre) + " para " + str(self.bodega_destino.nombre) + ' fecha:' + str(self.created_at)

    class Meta:
        verbose_name_plural = "Traslados"

class Saldo_Inicial(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.PROTECT)
    cantidad = models.FloatField(verbose_name="Cantidad")
    fecha = models.DateTimeField(verbose_name="Fecha")
    bodega = models.ForeignKey(Bodega, verbose_name="Bodega de Origen", on_delete=models.PROTECT)

    def __str__(self):
        return 'De ' + str(self.bodega.nombre) + " con " + str(self.producto.nombre) + ' fecha:' + str(self.fecha)

    class Meta:
        verbose_name_plural = "Saldo Inicial"

class Estado_Cierre(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Estado")

    def __str__(self):
        return str(self.nombre)

    class Meta:
        verbose_name_plural = "Estado del cierre"

class Cierre_Diario(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uui = models.UUIDField(default=uuid.uuid4, editable=False)
    total_operaciones_entrada = models.IntegerField(verbose_name='Total de operaciones de entrada')
    total_operaciones_salida = models.IntegerField(verbose_name='Total de operaciones de salida')
    dinero_depositar = models.FloatField(verbose_name="Dinero Total a depositar")
    fecha = models.DateTimeField(verbose_name="Fecha de cierre")
    estado_de_cierre = models.ForeignKey(Estado_Cierre, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.fecha)

    class Meta:
        verbose_name_plural = "Estado del cierre"