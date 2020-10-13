"""Bodega URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required, permission_required
from notifications import urls as notiURL
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as djangoViews
from rest_framework.authtoken import views as authviews
from BodegaApp import views, forms
from django.conf.urls.static import static
from rest_framework import routers
router = routers.DefaultRouter()
from ApiApp import urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/login/', views.loguear, name='ce_login'),
    path('', views.just_login, name='just_login'),
    path('logout/', views.logout, name='logout'),
    # path('api/', include(router.urls)),
    path('inicio_api/', include('ApiApp.urls'), name='inicio_api'),
    path('api_generate_token/',authviews.obtain_auth_token),

    # path('api-token-auth/ ', views.obtain_auth_token),
    # path('register/', views.register_front, name="register_front"),
    # path('register-by-url/<token>', views.register_by_url, name="register_by_url"),
    # path('administration', login_required(views.inicio), name="inicio"),
    path('backend/', login_required(views.inicio), name="inicio"),

    path('administration/grupo/list', login_required(views.group_list), name="group_list"),
    path('administration/grupo/create', login_required(views.group_create), name='group_create'),
    path('administration/grupo/update/<int:pk>',
         permission_required('bodegaApp.change_group', login_url='ce_login')(forms.GroupUpdate.as_view()),
         name='group_update'),
    path('administration/grupo/delete/<int:pk>/',
         permission_required('bodegaApp.delete_group', login_url='ce_login')(forms.GroupDelete.as_view()),
         name='group_delete'),
    path('administration/user/list', login_required(views.user_list), name="user_list"),
    path('administration/user/create', login_required(views.user_create), name='user_create'),
    path('administration/user/update/<int:pk>',
         permission_required('bodegaApp.change_user', login_url='ce_login')(forms.UserUpdate.as_view()),
         name='user_update'),
    path('administration/user/delete/<int:pk>/',
         permission_required('bodegaApp.delete_user', login_url='ce_login')(forms.UserDelete.as_view()),
         name='user_delete'),
    path('administration/password/update/<int:pk>/', login_required(views.password_update),
         name='password_update'),
# USUARIO
    path('user/password/reset/', views.PasswordResetView.as_view(),
         {'post_reset_redirect': '/user/password/reset/done/'}, name='password_reset'),
    path('user/password/reset/done/', djangoViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', djangoViews.PasswordResetConfirmView.as_view(),
         {'post_reset_redirect': '/user/reset/done/'}, name='password_reset_confirm'),
    path('user/reset/done/', djangoViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('good/count/activated', views.count_activated, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('user/update/<int:pk>', login_required(forms.UserUpdateAdmin.as_view()), name="profile"),


##·········································································································
### Provincia
    path('nomenclador/provincia/list', login_required(views.backend_provincia_listar),
         name="provincia_listar"),
    path('nomenclador/provincia/create', login_required(views.backend_provincia_agregar),
         name="provincia_create"),
    path('nomenclador/provincia/update/<int:pk>', login_required(forms.Update_Provincia.as_view()),
         name="provincia_update"),
    path('nomenclador/provincia/delete/<int:pk>', login_required(forms.Delete_Provincia.as_view()),
         name="provincia_delete"),
#### Municipio
    path('nomenclador/municipio/list', login_required(views.backend_municipio_listar),
         name="municipio_listar"),
    path('nomenclador/municipio/create', login_required(views.backend_municipio_agregar),
         name="municipio_create"),
    path('nomenclador/municipio/update/<int:pk>', login_required(forms.Update_Municipio.as_view()),
         name="municipio_update"),
    path('nomenclador/municipio/delete/<int:pk>', login_required(forms.Delete_Municipio.as_view()),
         name="municipio_delete"),

    #### Consejo
    path('nomenclador/consejo/list', login_required(views.backend_consejo_listar),
         name="consejo_listar"),
    path('nomenclador/consejo/create', login_required(views.backend_consejo_agregar),
         name="consejo_create"),
    path('nomenclador/consejo/update/<int:pk>', login_required(forms.Update_Consejo.as_view()),
         name="consejo_update"),
    path('nomenclador/consejo/delete/<int:pk>', login_required(forms.Delete_Consejo.as_view()),
         name="consejo_delete"),

    #### Zona
    path('nomenclador/zona/list', login_required(views.backend_zona_listar),
         name="zona_listar"),
    path('nomenclador/zona/create', login_required(views.backend_zona_agregar),
         name="zona_create"),
    path('nomenclador/zona/update/<int:pk>', login_required(forms.Update_Zona.as_view()),
         name="zona_update"),
    path('nomenclador/zona/delete/<int:pk>', login_required(forms.Delete_Zona.as_view()),
         name="zona_delete"),

    #### Clasificacion
    path('nomenclador/clasificacion/list', login_required(views.backend_clasificacion_listar),
         name="clasificacion_listar"),
    path('nomenclador/clasificacion/create', login_required(views.backend_clasificacion_agregar),
         name="clasificacion_create"),
    path('nomenclador/clasificacion/update/<int:pk>', login_required(forms.Update_Clasificacion.as_view()),
         name="clasificacion_update"),
    path('nomenclador/clasificacion/delete/<int:pk>', login_required(forms.Delete_Clasificacion.as_view()),
         name="clasificacion_delete"),

    #### UnidadMedida
    path('nomenclador/unidadmedida/list', login_required(views.backend_unidadmedida_listar),
         name="unidad_medida_listar"),
    path('nomenclador/unidadmedida/create', login_required(views.backend_unidadmedida_agregar),
         name="unidad_medida_create"),
    path('nomenclador/unidadmedida/update/<int:pk>', login_required(forms.Update_UnidadMedida.as_view()),
         name="unidad_medida_update"),
    path('nomenclador/unidadmedida/delete/<int:pk>', login_required(forms.Delete_UnidadMedida.as_view()),
         name="unidad_medida_delete"),

    #### TIPOD E OPERACION
    path('nomenclador/tipooperacion/list', login_required(views.backend_tipo_operacion_listar),
         name="tipo_operacion_listar"),
    path('nomenclador/tipooperacion/create', login_required(views.backend_tipo_operacion_agregar),
         name="tipo_operacion_create"),
    path('nomenclador/tipooperacion/update/<int:pk>', login_required(forms.Update_TipoOperacion.as_view()),
         name="tipo_operacion_update"),
    path('nomenclador/tipooperacion/delete/<int:pk>', login_required(forms.Delete_TipoOperacion.as_view()),
         name="tipo_operacion_delete"),
    #### Producto
    path('nomenclador/producto/list', login_required(views.backend_producto_listar),
         name="producto_listar"),
    path('nomenclador/producto/create', login_required(views.backend_producto_agregar),
         name="producto_create"),
    path('nomenclador/producto/update/<int:pk>', login_required(forms.Update_Producto.as_view()),
         name="producto_update"),
    path('nomenclador/producto/delete/<int:pk>', login_required(forms.Delete_Producto.as_view()),
         name="producto_delete"),

    #### Bodega
    path('nomenclador/bodega/list', login_required(views.backend_bodega_listar),
         name="bodega_listar"),
    path('nomenclador/bodega/create', login_required(views.backend_bodega_agregar),
         name="bodega_create"),
    path('nomenclador/bodega/update/<int:pk>', login_required(forms.Update_Bodega.as_view()),
         name="bodega_update"),
    path('nomenclador/bodega/delete/<int:pk>', login_required(forms.Delete_Bodega.as_view()),
         name="bodega_delete"),
    ######################## API ###################----------------------------------------------------------------
    # path('api/', include(router.urls)),
    # path('api-login/', views.LoginView.as_view()),
]

