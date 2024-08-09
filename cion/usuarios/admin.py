from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from catalogos.models import areas

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'apellido_materno', 'email', 'sexo', 'Municipio', 'areas', 'es_responsable')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'Municipio', 'sexo', 'areas', 'es_responsable'),
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'Municipio', 'sexo', 'es_responsable']
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
