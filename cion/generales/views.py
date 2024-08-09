from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Utiliza el mismo template para mostrar el formulario

    def form_invalid(self, form):
        # Display error message when credentials are invalid
        messages.error(self.request, 'Usuario o contraseña incorrecta. Por favor, inténtalo de nuevo.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('index')

def exit_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('index')
    
