from django.urls import path, include
from rest_framework import routers
from ApiApp import views
# from .views import UserViewSet

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('provincias-all', views.ProvinciaAllViewSet, basename="provincias_all")
router.register('municipios-all', views.MunicipioAllViewSet, basename="municipios_all")
router.register('bodega-productos', views.BodegaAllProductosViewSet, basename="bodega_productos")
urlpatterns = [
    # API APK
    path('v1/', include(router.urls)),
    # path('login/',UserViewSet),
    path('auth/', include('rest_framework.urls')),
]
