from django.urls import path
from .views import RegistroContribuyenteView, HomeContribuyente, ListContribuyentes, EditarContribuyenteView

urlpatterns = [
    path('home/', HomeContribuyente.as_view(), name='home_ctr'),
    path('lista_contribuyentes/', ListContribuyentes.as_view(), name='lista_ctr'),
    path('registro/', RegistroContribuyenteView.as_view(), name='registro_contribuyente'),
    path('editar_contribuyente/<int:pk>/', EditarContribuyenteView.as_view(), name='editar_contribuyente'),
]
