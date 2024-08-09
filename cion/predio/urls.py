from django.urls import path, include
from .views import *


urlpatterns = [
    path("homePredio/", homePredioView.as_view(),name='homePredio'),
    path("registrosPredio/", TablaRegistrosPredio.as_view(),name='registroPredios'),
    path("formularioPredio/", formularioPredio.as_view(),name='formularioPredio'),
    path('consultar-contribuyente/', consultar_contribuyente, name='consultar-contribuyente'),
    path('consultar-contribuyente_op/', consultar_contribuyente_op, name='consultar-contribuyente_op'),

    
    path('buscar-municipio/', buscar_municipio, name='buscar_municipio'),

    path('api/add-calle/', add_calle, name='add_calle'),
    path('api/add-calle-general/', add_calle_general, name='add_calle_general'),





    path('api/calles/<str:colonia_nombre>/', get_calles_by_colonia, name='get_calles_by_colonia'),
    path('api/calles-general/<str:estado_nombre>/<str:municipio_nombre>/<str:colonia_nombre>/', get_calles_by_colonia_general, name='get_calles_by_colonia_general'),



    path('verify-location/', verify_user_location, name='verify_location'),
    path('predio/actualizar/<int:pk>/', FormularioPredioUpdate.as_view(), name='actualizarPredio'),


]