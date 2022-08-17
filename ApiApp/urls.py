from django.urls import path

from ApiApp import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('bodega/productos/', views.ProductosBodega.as_view({'get': 'list'}), name='productos_bodega'),
    path('unidad-medida/', views.UnidadMedidaList.as_view({'get': 'list'}), name='unidad_medida_list'),
    path('clasificacion/', views.ClasificacionList.as_view({'get': 'list'}), name='clasificacion_list'),
    path('tipo-operacion/', views.TipoOperacionList.as_view({'get': 'list'}), name='tipo_operacion_list'),
    path('seccion-operacion/', views.SeccionOperacionList.as_view({'get': 'list'}), name='seccion_operacion_list')
]
