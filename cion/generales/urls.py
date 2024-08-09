from django.urls import path, include
from .views import CustomLoginView, exit_view
urlpatterns = [
    path("", CustomLoginView.as_view(),name='login'),
    path("exit", exit_view, name='exit'),

]