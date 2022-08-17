from django.core import exceptions
from django.contrib.auth import authenticate
from rest_framework import serializers
from BodegaApp.models import *
#INFO
#En serializer se especifican las clases de lo que se recibe o lo que se manda
#un ejemplo de lo que se recibe es LoginSerializer
#un ejemplo de lo que se manda BodegaProductosSerializer
#es la forma que tiene rest framwork de validar los datos de transferencias.


#En la funcion loguin, autenticamos al usuario y le creamos un token en ese instante
#token que usara la apk para el consumo del api, SEGURIDAD
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = {"msg":"Usuario desactivado"}
                    raise exceptions.ValidationError(msg)
            else:
                user = User.objects.filter(username=username)
                if user.count() > 0:
                    if not user.get().is_active:
                        msg = {"msg": "Usuario pendiente de activación"}
                        raise exceptions.ValidationError(msg)
                    else:
                        msg = {"msg": "Error en el login, credenciales erroneas."}
                        raise exceptions.ValidationError(msg)
                else:
                    msg = {"msg":"Error en el login, credenciales erroneas."}
                    raise exceptions.ValidationError(msg)
        else:
            msg = {"msg":"Debe escribir usuario o contraseña, los dos!"}
            raise exceptions.ValidationError(msg)
        return data

#Se serializa la bodega del administrador, mas los productos que posee
class BodegaProductosSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    # zona = serializers.SerializerMethodField()
    # consejo = serializers.SerializerMethodField()
    # municipio = serializers.SerializerMethodField()
    # provincia = serializers.SerializerMethodField()

    class Meta:
        model = Bodega
        fields = ('uui',
                  # 'created_at',
                  # 'updated_at',
                  'nombre',
                  'admin',
                  # 'zona',
                  # 'consejo',
                  # 'municipio',
                  # 'provincia',
                  'productos'
                  )

    # def get_zona(self, obj):
    #     res = {}
    #     res['uui'] = obj.zona.uui
    #     res['nombre'] = obj.zona.nombre
    #     return res

    # def get_consejo(self, obj):
    #     res = {}
    #     res['uui'] = obj.zona.consejo.uui
    #     res['nombre'] = obj.zona.consejo.nombre
    #     return res

    # def get_municipio(self, obj):
    #     res = {}
    #     res['uui'] = obj.zona.consejo.municipio.uui
    #     res['nombre'] = obj.zona.consejo.municipio.nombre
    #     return res

    # def get_provincia(self, obj):
    #     res = {}
    #     res['uui'] = obj.zona.consejo.municipio.provincia.uui
    #     res['nombre'] = obj.zona.consejo.municipio.provincia.nombre
    #     return res

    def get_productos(self, obj):
        array = []
        for p in obj.productos.all():
            dict = {}
            dict["uui"] = p.uui
            dict["created_at"] = p.created_at
            dict["updated_at"] = p.updated_at
            dict["codigo"] = p.codigo
            dict["precio_venta"] = p.precio_venta
            dict["unidad"] = p.unidad.uui
            dict["clasificacion"] = p.clasificacion.uui
            dict["nombre"] = p.nombre
            preciosCostoArray = []
            preciosCosto = ProdPrecioCosto.objects.filter(producto__id=p.id).order_by('-fecha').all()
            for pc in preciosCosto:
                pc_dict = {}
                pc_dict['uui'] = pc.uui
                pc_dict['valor'] = pc.valor
                pc_dict['fecha'] = pc.fecha
                preciosCostoArray.append(pc_dict)
            dict['preciosCosto'] = preciosCostoArray
            array.append(dict)
        return array


#Nomencladores
class UnidadMedidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnidadMedida
        fields = ('uui', 'nombre')

class ClasificacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clasificacion
        fields = ('uui', 'nombre')

class TipoOperacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoOperacion
        fields = ('uui', 'nombre')

class SeccionOperacionSerializer(serializers.ModelSerializer):
    tipo_operacion = serializers.SerializerMethodField()

    class Meta:
        model = SeccionOperacion
        fields = ('uui', 'nombre', 'tipo_operacion')

    def get_tipo_operacion(self, obj):
        return obj.tipo_operacion.uui