from django.urls import path, include
from .views import CreateOrdenPago, HomeOrdenesPago, GenerarPDF, cobroSAgua, BAdeudos, buscar_contribuyente_deuda, get_areas, get_servicios_por_area,tablaDeuda, info_adeudo2, info_adeudo_predio
urlpatterns = [
    path('cobro_agua/', cobroSAgua.as_view(), name='cobro_agua'),
    path('home/', HomeOrdenesPago.as_view(), name='home_odp' ),
    path('orden/', GenerarPDF.as_view(), name='generar-pdf'),
    path('busqueda_adeudo/', BAdeudos.as_view(), name='busqueda_adeudo'),
    path('buscar_contribuyente_deuda/', buscar_contribuyente_deuda, name='buscar_contribuyente_deuda'),
    path('info_adeudo/', tablaDeuda.as_view(), name='info_adeudo'),
    path('info_adeudo2/', info_adeudo2, name='info_adeudo2'),
    path('info_adeudo_predio/', info_adeudo_predio, name='info_adeudo_predio'),
    path('crear-orden-pago/', CreateOrdenPago.as_view(), name='create_orden_pago' ),
    path('crear-orden-pago/', CreateOrdenPago.as_view(), name='create_orden_pago' ),



    path('obtener-areas/', get_areas, name='get_areas'),
    path('get_servicios_por_area/<int:area_id>/', get_servicios_por_area, name='get_servicios_por_area'),

]