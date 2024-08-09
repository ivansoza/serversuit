from django.urls import path
from .views import homeOdp, tablaregistrosDocsODP, formRegistrosDocsODP, EditarRegistroView, tablasAreas, document_info
urlpatterns = [
        path("inicioODP/", homeOdp.as_view(),name='inicioODP'),
        path("registrosODP/", tablaregistrosDocsODP.as_view(),name='registrosODP'),
        path("formularioODP/", formRegistrosDocsODP.as_view(),name='formularioODP'),
        path('editar/<int:pk>/', EditarRegistroView.as_view(), name='editar_registro'),
        path("areasODP/", tablasAreas.as_view(),name='areasODP'),
        path('url-to-fetch-document-info/<int:id>/', document_info, name='document_info'),

]