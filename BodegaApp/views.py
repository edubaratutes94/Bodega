import subprocess
import uuid
from datetime import date

from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import logout_then_login, PasswordContextMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView
from notifications import models as models_notify
from notifications.signals import notify
from django.shortcuts import redirect
from BodegaApp import models, forms
# from BodegaApp.forms import *
from BodegaApp.utils import register_logs, list_address_db, save_address_dbs
from django.utils.translation import ugettext_lazy as _
from BodegaApp.token import account_activation_token


def inicio(request):
    return render(request, "inicio.html")

def just_login(request):
    response = HttpResponseRedirect('/accounts/login/')
    response.delete_cookie('user')
    response.delete_cookie('user_photo')
    return response

# @api_view('GET')
def loguear(request):
    # dir_ip = request.META['REMOTE_ADDR']
    # dir_ip = request.META['HTTP_X_FORWARDED_FOR']
    mensage = ''
    if request.method == 'POST':
        user = request.POST['username']
        passw = request.POST['password']
        access = authenticate(username=user, password=passw)
        if access is not None:
            if access.is_active:
                login(request, access)
                # userApp = models.UserApp.objects.filter(pk=request.user.pk).first
                userApp = models.UserApp.objects.get(pk=request.user.pk)
                register_logs(request, User, "", "", 4)
                messages.success(request, "Usted se ha logueado con éxito")
                response = HttpResponseRedirect('/backend')
                response.set_cookie("user", request.user.username)

                if userApp.image:
                    response.set_cookie("user_photo", userApp.image)
                else:
                    response.set_cookie("user_photo", "static/users/userDefault4.png")
                return response
            else:
                messages.error(request, "Usuario inactivo")
        else:
            messages.error(request, "Nombre de usuario y/o contraseña inválidos")
    if request.COOKIES.get("user"):
        username = request.COOKIES.get("user")
        userPhoto = request.COOKIES.get("user_photo")
        return render(request, "Authentication/login.html", {"username": username, "user_photo": userPhoto})
    return render(request, 'Authentication/login.html')


def count_activated(request):
    return render(request, 'registration/good_message_activated.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, _("Usuario activado correctamente"))
        return redirect('inicio')
    else:
        return render(request, 'registration/error_message_activated.html')


def logout(request):
    register_logs(request, User, "", "", 5)
    return logout_then_login(request, 'ce_login')

def notificacion_read(request, action):
    if request.GET:
        id = request.GET['id']
        notification = models_notify.Notification.objects.get(pk=id)
        notification.unread = False
        notification.save()
        if action == 1:
            notifications = models_notify.Notification.objects.filter(recipient_id=request.user.id).filter(
                unread=True).exclude(description="comments").all()
            return render(request, 'Ajax/notifications.html', {"notifications": notifications})
        if action == 2:
            notifications = models_notify.Notification.objects.filter(recipient_id=request.user.id).filter(
                unread=True).filter(description="comments")
            return render(request, 'Ajax/notifications.html', {"notifications": notifications, "one": "1"})

def notification_offer_all_mark_read(request):
    noti = models_notify.Notification.objects.exclude(description=None).filter(recipient_id=request.user.id)
    if noti.count() > 0:
        for n in noti:
            n.unread = False
            n.save()
    return render(request, 'Ajax/notifications.html')

def notification_all_mark_read(request):
    noti = models_notify.Notification.objects.filter(description=None, recipient_id=request.user.id)
    if noti.count() > 0:
        for n in noti:
            n.unread = False
            n.save()
    return render(request, 'Ajax/notifications.html')

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = "Proyecto <hola@gmail.com>"
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Resetear Contraseña')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

@permission_required('auth.add_group')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'Security/groups.html', {'group_list': groups})

def error404(request):
    return render(request, "Security/404.html")

# CRUD Rol
@permission_required('auth.add_group')
def group_create(request):
    if request.POST:
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            form.save()
            id_group = Group.objects.last()
            register_logs(request, Group, id_group.pk, id_group.__str__(), 1)
            messages.success(request, "Rol creado con éxito")
            return HttpResponseRedirect('/administration/grupo/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.GroupForm()
    args = {}
    args['form'] = form
    return render(request, 'auth/group_form.html', args)

@permission_required('auth.add_user')
def user_list(request):
    users_list = User.objects.filter(is_superuser=False).order_by("-date_joined")
    users = []
    for user in users_list:
        users.append([user, None])
    return render(request, 'Security/users.html', {'usersList': users})


@permission_required('auth.add_user')
def user_create(request):
    if request.POST:
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()
            id_user = User.objects.last()
            register_logs(request, User, id_user.pk, id_user.__str__(), 1)
            notify.send(request.user, recipient=id_user, verb='Bienvenido a Proyecto!!', level='success')
            messages.success(request, "Usuario creado con éxito")
            return HttpResponseRedirect('/administration/user/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.UserForm()
    args = {}
    args['form'] = form
    return render(request, 'auth/user_form.html', args)


@permission_required('auth.change_user')
def password_update(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            register_logs(request, User, user.pk, user.__str__(), 2)
            notify.send(request.user, recipient=user, verb='Se ha cambiado su contraseña', level='warning')
            update_session_auth_hash(request, form.user)
            messages.success(request, "Contraseña actualizada correctamente")
            return HttpResponseRedirect('/user/update/' + str(user.pk))
        else:
            messages.error(request, "Error cambiando contraseña, rectifique los datos")
            form = PasswordChangeForm(user=user, data=request.POST)
            return render(request, 'Security/Auth/password_update.html', {'form': form})
    else:
        form = PasswordChangeForm(user=user, data=request.POST)
        return render(request, 'Security/Auth/password_update.html', {'form': form, 'user': user})



############################################"""""""""""""BODEGA"""""""""""""""""""##################################

# PROVINCIA
@permission_required('BodegaApp.add_provincia')
def backend_provincia_listar(request):
    provincia = models.Provincia.objects.all()
    return render(request, 'backend/provincia.html', {'provincia': provincia})

@permission_required('BodegaApp.add_provincia')
def backend_provincia_agregar(request):
    if request.POST:
        form = forms.Form_Provincia(request.POST)
        if form.is_valid():
            form.save()
            x = models.Provincia.objects.last()
            register_logs(request, models.Provincia, x.pk, x.__str__(), 1)
            messages.success(request, "Provincia creada con éxito")
            return HttpResponseRedirect('/nomenclador/provincia/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Provincia()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/provincia_form.html', args)


# MUNICIPIOS
@permission_required('BodegaApp.add_provincia')
def backend_municipio_listar(request):
    municipio = models.Municipio.objects.all()
    return render(request, 'backend/municipio.html', {'municipio': municipio})

@permission_required('BodegaApp.add_provincia')
def backend_municipio_agregar(request):
    if request.POST:
        form = forms.Form_Municipio(request.POST)
        if form.is_valid():
            form.save()
            x = models.Municipio.objects.last()
            register_logs(request, models.Municipio, x.pk, x.__str__(), 1)
            messages.success(request, "Municipio creado con éxito")
            return HttpResponseRedirect('/nomenclador/municipio/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Municipio()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/municipio_form.html', args)



# CONSEJO POPULAR
@permission_required('BodegaApp.add_provincia')
def backend_consejo_listar(request):
    consejo = models.ConsejoPopular.objects.all()
    return render(request, 'backend/consejopopular.html', {'consejo': consejo})

@permission_required('BodegaApp.add_provincia')
def backend_consejo_agregar(request):
    if request.POST:
        form = forms.Form_Consejo(request.POST)
        if form.is_valid():
            form.save()
            x = models.ConsejoPopular.objects.last()
            register_logs(request, models.ConsejoPopular, x.pk, x.__str__(), 1)
            messages.success(request, "Consejo creado con éxito")
            return HttpResponseRedirect('/nomenclador/consejo/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Consejo()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/consejo_form.html', args)


# ZONAAA
@permission_required('BodegaApp.add_provincia')
def backend_zona_listar(request):
    zona = models.Zona.objects.all()
    return render(request, 'backend/zona.html', {'zona': zona})

@permission_required('BodegaApp.add_provincia')
def backend_zona_agregar(request):
    if request.POST:
        form = forms.Form_Zona(request.POST)
        if form.is_valid():
            form.save()
            x = models.Zona.objects.last()
            register_logs(request, models.Zona, x.pk, x.__str__(), 1)
            messages.success(request, "Zona creada con éxito")
            return HttpResponseRedirect('/nomenclador/zona/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Zona()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/zona_form.html', args)

# CLASIFICACION
@permission_required('BodegaApp.add_provincia')
def backend_clasificacion_listar(request):
    clasificacion = models.Clasificacion.objects.all()
    return render(request, 'backend/clasificacion.html', {'clasificacion': clasificacion})

@permission_required('BodegaApp.add_provincia')
def backend_clasificacion_agregar(request):
    if request.POST:
        form = forms.Form_Clasificacion(request.POST)
        if form.is_valid():
            form.save()
            x = models.Clasificacion.objects.last()
            register_logs(request, models.Clasificacion, x.pk, x.__str__(), 1)
            messages.success(request, "Clasificación creada con éxito")
            return HttpResponseRedirect('/nomenclador/clasificacion/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Clasificacion()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/clasificacion_form.html', args)



    # UnIDAD DE EDIDA


@permission_required('BodegaApp.add_provincia')
def backend_unidadmedida_listar(request):
    unidadmedida = models.UnidadMedida.objects.all()
    return render(request, 'backend/unidad_medida.html', {'unidadmedida': unidadmedida})

@permission_required('BodegaApp.add_provincia')
def backend_unidadmedida_agregar(request):
    if request.POST:
        form = forms.Form_UnidadMedida(request.POST)
        if form.is_valid():
            form.save()
            x = models.UnidadMedida.objects.last()
            register_logs(request, models.UnidadMedida, x.pk, x.__str__(), 1)
            messages.success(request, "Unidad de Medida creada con éxito")
            return HttpResponseRedirect('/nomenclador/unidadmedida/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_UnidadMedida()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/unidad_medida_form.html', args)



    # TIPO DE OPOERACION


@permission_required('BodegaApp.add_provincia')
def backend_tipo_operacion_listar(request):
    tipo_operacion = models.TipoOperacion.objects.all()
    return render(request, 'backend/tipo_operacion.html', {'tipo_operacion': tipo_operacion})

@permission_required('BodegaApp.add_provincia')
def backend_tipo_operacion_agregar(request):
    if request.POST:
        form = forms.Form_TipoOperacion(request.POST)
        if form.is_valid():
            form.save()
            x = models.TipoOperacion.objects.last()
            register_logs(request, models.TipoOperacion, x.pk, x.__str__(), 1)
            messages.success(request, "Tipo de Operación creada con éxito")
            return HttpResponseRedirect('/nomenclador/tipooperacion/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_TipoOperacion()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/tipo_operacion_form.html', args)


# Producto
@permission_required('BodegaApp.add_provincia')
def backend_producto_listar(request):
    producto = models.Producto.objects.all()
    return render(request, 'backend/producto.html', {'producto': producto})

@permission_required('BodegaApp.add_provincia')
def backend_producto_agregar(request):
    if request.POST:
        form = forms.Form_Producto(request.POST)
        if form.is_valid():
            form.save()
            x = models.Producto.objects.last()
            register_logs(request, models.Producto, x.pk, x.__str__(), 1)
            messages.success(request, "Producto creado con éxito")
            return HttpResponseRedirect('/nomenclador/producto/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Producto()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/producto_form.html', args)


# Bodega
@permission_required('BodegaApp.add_provincia')
def backend_bodega_listar(request):
    bodega = models.Bodega.objects.all()
    return render(request, 'backend/bodega.html', {'bodega': bodega})

@permission_required('BodegaApp.add_provincia')
def backend_bodega_agregar(request):
    if request.POST:
        form = forms.Form_Bodega(request.POST)
        if form.is_valid():
            form.save()
            x = models.Bodega.objects.last()
            register_logs(request, models.Bodega, x.pk, x.__str__(), 1)
            messages.success(request, "Bodega creada con éxito")
            return HttpResponseRedirect('/nomenclador/bodega/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_Bodega()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/bodega_form.html', args)



# NOTIGNERAKL
@permission_required('BodegaApp.add_provincia')
def backend_noti_listar(request):
    notificacion = models.Notificacion_general.objects.all()
    return render(request, 'backend/notificacion.html', {'notificacion': notificacion})

@permission_required('BodegaApp.add_provincia')
def backend_noti_agregar(request):
    if request.POST:
        form = forms.Form_NotiGeneral(request.POST)
        if form.is_valid():
            form.save()
            x = models.Notificacion_general.objects.last()
            register_logs(request, models.Notificacion_general, x.pk, x.__str__(), 1)
            messages.success(request, "Notificación creada con éxito")
            return HttpResponseRedirect('/nomenclador/notificacion/list')
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = forms.Form_NotiGeneral()
    args = {}
    args['form'] = form
    return render(request, 'BodegaApp/notificacion_form.html', args)

