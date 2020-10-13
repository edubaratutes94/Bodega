from django.urls import path, include
from rest_framework import routers
from ApiApp import views

router = routers.DefaultRouter()

router.register('provincias-all', views.ProvinciaAllViewSet, basename="provincias_all")
router.register('municipios-all', views.MunicipioAllViewSet, basename="municipios_all")
urlpatterns = [
    # API APK
    path('api/', include(router.urls)),
    path('api_login/', views.LoginView.as_view()),

]
