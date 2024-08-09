from django.urls import path, include
from .views import ConfiguracionView, CustomUserCreateView, CustomUserListView, PasswordChangeView, PersonalizacionInfoView, PersonalizacionView, actualizar_personalizacion1, homeCatalogos, subir_imagen_inicio, subir_imagen_organigrama, subir_logotipo, tablaDescuentos, eliminar_descuento, editar_descuento
from .views import obtener_registro, tablaArea, tablaServicios, editar_servicio, obtener_registro_servicio, editar_servicio

from .views import PersonalizacionView, actualizar_personalizacion1, subir_logotipo, homeCatalogos
urlpatterns = [

    path('', PersonalizacionView.as_view(),name='personalizacion'),
    path('personalizacionInformacion', PersonalizacionInfoView.as_view(),name='PersonalizacionInfoView'),

    path('actualizar_personalizacion/', actualizar_personalizacion1, name='actualizar_personalizacion1'),
    path('subir-logotipo/', subir_logotipo, name='subir_logotipo'),
    path('subir-fondo/', subir_imagen_inicio, name='subir_fondo'),
    path('subir-organigrama/', subir_imagen_organigrama, name='subir_organigrama'),
    path('homeCatalogos/', homeCatalogos.as_view(),name='homeCatalogos'),
    path('tablaDescuentos/', tablaDescuentos.as_view(),name='tablaDescuentos'),
    path('eliminar_descuento/<int:id>/', eliminar_descuento, name='eliminar_descuento'),
    path('editar_descuento/<int:id>/', editar_descuento, name='editarDescuento'),
    path('obtener_registro/<int:id>/', obtener_registro, name='obtener_registro'),
    path('tablaArea/', tablaArea.as_view(),name='tablaArea'),
    path('tablaServicios/', tablaServicios.as_view(),name='tablaServicios'),
    path('editar_servicio/<int:id>/', editar_servicio, name='editar_servicio'),
    path('obtener_registro_servicio/<int:id>/', obtener_registro_servicio, name='obtener_registro_servicio'),    
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('usuarios/', CustomUserListView.as_view(), name='customuser_list'),
    path('configuracion/', ConfiguracionView.as_view(), name='configuracion'),
    path('configuracion/cambiar-contraseña/', PasswordChangeView.as_view(), name='cambiar_contraseña'),



]
