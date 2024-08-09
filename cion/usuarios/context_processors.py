from django.conf import settings
from catalogos.models import PersonalizacionTema
from django.contrib.auth import get_user_model
from django.templatetags.static import static
from cionapp.models import PaginaInicio

def personalizacion_context(request):
    contexto = {
        'tiene_municipio': False,
        'tiene_personalizacion': False,
        'personalizacion': None
    }
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'Municipio') and request.user.Municipio is not None:
            contexto['tiene_municipio'] = True
            municipio = request.user.Municipio
            try:
                personalizacion = PersonalizacionTema.objects.get(municipio=municipio)
                contexto['tiene_personalizacion'] = True
                contexto['personalizacion'] = {
                    'tipo_diseno': personalizacion.tipo_diseno,
                    'tipo_sidebar': personalizacion.tipo_sidebar,
                    'tipo_icono_sidebar': personalizacion.tipo_icono_sidebar,
                    'color_primario': personalizacion.color_1,
                    'color_primario_a': personalizacion.color_1a,

                    'color_secundario': personalizacion.color_2,
                    'color_secundario_a': personalizacion.color_2a,
                    'logotipo_url': personalizacion.logotipo.url if personalizacion.logotipo else None


                }
            except PersonalizacionTema.DoesNotExist:
                contexto['tiene_personalizacion'] = False

    return contexto




def user_info(request):
    # Imágenes por defecto para cuando no hay usuario autenticado o no se define el sexo
    default_image_url = static('assets/images/user/usuariono.png')
    default_image_url_new = static('assets/images/user/usermale300.png')  # Default male image for new URL

    # Inicializa las variables con valores por defecto
    user_name = "Usuario Anónimo"
    email = "No definido"

    if request.user.is_authenticated:
        user = get_user_model().objects.get(username=request.user.username)
        if user.sexo == 'masculino':
            image_url = static('assets/images/user/usuariono.png')
            user_image_url_new = static('assets/images/user/usermale300.png')
        elif user.sexo == 'femenino':
            image_url = static('assets/images/user/usuariono1.png')
            user_image_url_new = static('assets/images/user/userfemale300.png')
        else:
            # Si no está definido el sexo, usar imágenes por defecto
            image_url = default_image_url
            user_image_url_new = default_image_url_new

        user_name = user.username
        email = user.email if user.email else "No definido"
    else:
        # Si el usuario no está autenticado, usar imágenes por defecto
        image_url = default_image_url
        user_image_url_new = default_image_url_new

    return {
        'user_name': user_name,
        'user_image_url': image_url,
        'user_image_url_new': user_image_url_new,
        'user_email': email
    }
def pagina_inicio_context(request):
    contexto = {
        'pagina_inicio_titulo': None
    }
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'Municipio') and request.user.Municipio is not None:
            municipio = request.user.Municipio
            try:
                pagina_inicio = PaginaInicio.objects.get(municipio=municipio)
                contexto['pagina_inicio_titulo'] = pagina_inicio.titulo
            except PaginaInicio.DoesNotExist:
                contexto['pagina_inicio_titulo'] = None

    return contexto


def user_full_name(request):
    if not request.user.is_authenticated:
        return {}  

    user = request.user
    full_name_parts = []

    if user.first_name:
        full_name_parts.append(user.first_name.title())
    if user.last_name:
        full_name_parts.append(user.last_name.title())
    if hasattr(user, 'apellido_materno') and user.apellido_materno:
        full_name_parts.append(user.apellido_materno.title())

    full_name = ' '.join(full_name_parts) if full_name_parts else user.username.title()

    return {'user_full_name': full_name}

def user_first_name(request):
    if not request.user.is_authenticated:
        return {}

    first_name = request.user.first_name.title() if request.user.first_name else "Usuario"
    
    return {'user_first_name': first_name}