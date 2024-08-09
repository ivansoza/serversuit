from django.urls import path, include
from .views import *
urlpatterns = [
    path("homeAgua/", homeAguaView.as_view(),name='homeAgua'),
    path("formularioAgua/", formularioAgua.as_view(),name='formularioAgua'),
    path("registrosAgua/", TablaRegistrosAgua.as_view(),name='registrosAgua'),
    path('buscar_contribuyente/', buscar_contribuyente, name='buscar_contribuyente'),
    path('eliminar/<int:id>/', eliminar_no_servicio, name='eliminar_servicio'),
    path('editar_servicio/<int:pk>/', editar_noServicio, name='editar_servicio'),
    path('buscar_predio/', buscar_predio, name='buscar_predio'),
    path('cobroAgua/', cobroAgua.as_view(), name='cobroAgua'),
    path('obtener_predios/', obtener_predios, name='obtener_predios'),
    path('obtener_predio_detalle/', obtener_predio_detalle, name='obtener_predio_detalle'),

]