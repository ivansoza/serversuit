from django.urls import path
from . import views 
from .views import op,tablaOP,eliminar_odp,EditarODPView,obtener_formulario_edicion,atender_odp,AtendidosListView,ODPListView,AtendidoListView,guardar_revision_propuesta

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
urlpatterns = [
    path('op', op.as_view(), name='oficialia_de_partes'),
    path('tablaOP', tablaOP.as_view(), name='tablaOP'),
    path('editar/<int:pk>/', EditarODPView.as_view(), name='editar_odp'),
    path('obtener_formulario_edicion/<int:pk>/', obtener_formulario_edicion, name='obtener_formulario_edicion'),
    path('eliminar/<int:pk>/', eliminar_odp, name='eliminar_odp'),
    path('atender/<int:odp_id>/', atender_odp, name='atender_odp'),
    path('atendidos/', AtendidosListView.as_view(), name='atendidos_list'),
    path('lista_odp/', ODPListView.as_view(), name='lista_odp'),
    path('revisions/', AtendidoListView.as_view(), name='revision_list'),
    path('guardar_revision_propuesta/<int:atendido_id>/', guardar_revision_propuesta, name='guardar_revision_propuesta'),

]
