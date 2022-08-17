from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.contrib.auth.models import Group,User
from django.views.generic import UpdateView
from django.views.generic.edit import BaseUpdateView, DeleteView
from notifications.signals import notify
from PIL import Image
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.forms import widgets, TextInput, Textarea, EmailInput
from django.http import HttpResponseRedirect

from BodegaApp import models
from BodegaApp.utils import register_logs

class SignUpForm(UserCreationForm):
    # captcha = CaptchaField()
    email = forms.EmailField(max_length=254)

    class Meta:
        model = models.UserApp
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Correo'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Su Nombre'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sus Apellidos'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].widget.attrs['minlength'] = '8'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita la Contraseña'
        self.fields['password2'].widget.attrs['minlength'] = '8'
        self.fields['captcha'].widget.attrs['class'] = 'form-control'
        self.fields['captcha'].widget.attrs['placeholder'] = 'Captcha'

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            if len(str(email).split("gmail")) > 1:
                if len(str(email).split("+")) > 1:
                    part = str(email).split("@")
                    if len(part) > 1:
                        email = str(part[0]).split("+")[0] + str(part[1])
            match = models.UserApp.objects.get(email=email)
        except models.UserApp.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('Este email ya esta en uso.')

    def clean_username(self):
        # Get the email
        usernam = self.cleaned_data.get('username')

        # Check to see if any users already exist with this email as a username.
        try:
            match = models.UserApp.objects.get(username=usernam)
        except models.UserApp.DoesNotExist:
            # Unable to find a user, this is fine
            return usernam

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('Este nombre de usuario ya esta en uso')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        widgets = {
            "name": widgets.TextInput(attrs={'class': ' form-control'}),
            "permissions": widgets.SelectMultiple(attrs={'class': ' form-control', 'placeholder': 'Rol',
                                                         'style': 'height: 400px'}),
        }


class GroupUpdate(UpdateView):
    form_class = GroupForm
    model = Group
    success_url = reverse_lazy('group_list')

    def post(self, request, *args, **kwargs):
        register_logs(request, Group, self.get_object().pk, self.get_object().__str__(), 2)
        self.object = self.get_object()
        messages.success(request, "Rol modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)


class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')

    def delete(self, request, *args, **kwargs):
        register_logs(request, Group, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Rol eliminado con éxito")
        return HttpResponseRedirect(success_url)


class UserForm(UserCreationForm):
    # captcha = CaptchaField()
    class Meta:
        model = models.UserApp
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'groups'
        ]
        widgets = {
            "username": widgets.TextInput(attrs={'class': ' form-control'}),
            "first_name": widgets.TextInput(attrs={'class': ' form-control'}),
            "last_name": widgets.TextInput(attrs={'class': ' form-control'}),
            "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            "password1": widgets.PasswordInput(attrs={'class': ' form-control'}),
            "password2": widgets.PasswordInput(attrs={'class': ' form-control'}),
            "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
        }

class UserProfile(forms.ModelForm):
    class Meta:
        model = models.UserApp
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'image',
        ]
        widgets = {
            "username": widgets.TextInput(attrs={'class': ' form-control'}),
            "first_name": widgets.TextInput(attrs={'class': ' form-control','required':'required'}),
            "last_name": widgets.TextInput(attrs={'class': ' form-control','required':'required'}),
            "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            "image": widgets.ClearableFileInput(attrs={'class': ' form-control'}),
        }

class UserAdminProfile(forms.ModelForm):
    class Meta:
        model = models.UserApp
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'is_active',
            'image',
        ]
        widgets = {
            "username": widgets.TextInput(attrs={'class': ' form-control'}),
            "first_name": widgets.TextInput(attrs={'class': ' form-control','required':'required'}),
            "last_name": widgets.TextInput(attrs={'class': ' form-control','required':'required'}),
            "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            "image": widgets.ClearableFileInput(attrs={'class': ' form-control'}),
        }

class UserUpdateAdmin(UpdateView):
    model = models.UserApp
    form_class = UserProfile
    template_name = ('auth/profile.html')
    success_url = reverse_lazy('inicio')

    def get(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().pk:
            self.object = self.get_object()
            return super(BaseUpdateView, self).get(request, *args, **kwargs)
        else:
            return render(request,'Security/404.html')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.UserApp, self.get_object().uui, self.get_object().__str__(), 2)
        notify.send(request.user, recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Usuario modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            if self.request.POST.get('x') != "":
                x = float(self.request.POST.get('x'))
                y = float(self.request.POST.get('y'))
                w = float(self.request.POST.get('width'))
                h = float(self.request.POST.get('height'))

                image = Image.open(self.get_object().image)
                cropped_image = image.crop((x, y, w + x, h + y))
                resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
                resized_image.save(self.get_object().image.path)
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

class UserUpdate(UpdateView):
    model = models.UserApp
    form_class = UserAdminProfile
    template_name = ('auth/user_form.html')
    success_url = reverse_lazy('user_list')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.UserApp, self.get_object().uui, self.get_object().__str__(), 2)
        notify.send(request.user, recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Usuario modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.UserApp, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Usuario eliminado con éxito")
        return HttpResponseRedirect(success_url)




# Provincias

class Form_Provincia(forms.ModelForm):
    class Meta:
        model = models.Provincia
        fields = [
            'nombre',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),

        }


class Update_Provincia(UpdateView):
    model = models.Provincia
    form_class = Form_Provincia
    template_name = ('BodegaApp/provincia_form.html')
    success_url = reverse_lazy('provincia_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Provincia, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request,'Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Provincia modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Provincia(DeleteView):
    model = models.Provincia
    template_name = ('BodegaApp/provincia_confirm_delete.html')
    success_url = reverse_lazy('provincia_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Provincia, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Provincia eliminada con éxito")
        return HttpResponseRedirect(success_url)

# FORM Municipio

class Form_Municipio(forms.ModelForm):
    class Meta:
        model = models.Municipio
        fields = [
            'nombre',
            'provincia',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            "provincia": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_Municipio(UpdateView):
    model = models.Municipio
    form_class = Form_Municipio
    template_name = ('BodegaApp/municipio_form.html')
    success_url = reverse_lazy('municipio_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Municipio, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Municipio modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Municipio(DeleteView):
    model = models.Municipio
    success_url = reverse_lazy('municipio_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Municipio, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Municipio eliminado con éxito")
        return HttpResponseRedirect(success_url)


# FORM Consejo

class Form_Consejo(forms.ModelForm):
    class Meta:
        model = models.ConsejoPopular
        fields = [
            'nombre',
            'municipio',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            "municipio": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_Consejo(UpdateView):
    model = models.ConsejoPopular
    form_class = Form_Consejo
    template_name = ('BodegaApp/consejo_form.html')
    success_url = reverse_lazy('consejo_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.ConsejoPopular, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Consejo modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Consejo(DeleteView):
    model = models.ConsejoPopular
    success_url = reverse_lazy('consejo_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.ConsejoPopular, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Consejo eliminado con éxito")
        return HttpResponseRedirect(success_url)


# FORM ZOna

class Form_Zona(forms.ModelForm):
    class Meta:
        model = models.Zona
        fields = [
            'nombre',
            'consejo',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            "consejo": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_Zona(UpdateView):
    model = models.Zona
    form_class = Form_Zona
    template_name = ('BodegaApp/zona_form.html')
    success_url = reverse_lazy('zona_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Zona, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Zona modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Zona(DeleteView):
    model = models.Zona
    success_url = reverse_lazy('zona_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Zona, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Zona eliminada con éxito")
        return HttpResponseRedirect(success_url)


    ### CLASIFICACION
class Form_Clasificacion(forms.ModelForm):
    class Meta:
        model = models.Clasificacion
        fields = [
            'nombre',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_Clasificacion(UpdateView):
    model = models.Clasificacion
    form_class = Form_Clasificacion
    template_name = ('BodegaApp/clasificacion_form.html')
    success_url = reverse_lazy('clasificacion_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Clasificacion, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Clasificación modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Clasificacion(DeleteView):
    model = models.Clasificacion
    success_url = reverse_lazy('clasificacion_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Clasificacion, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Clasificación eliminada con éxito")
        return HttpResponseRedirect(success_url)



### UNIDD E MEDIDA
class Form_UnidadMedida(forms.ModelForm):
    class Meta:
        model = models.UnidadMedida
        fields = [
            'nombre',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_UnidadMedida(UpdateView):
    model = models.UnidadMedida
    form_class = Form_UnidadMedida
    template_name = ('BodegaApp/unidad_medida_form.html')
    success_url = reverse_lazy('unidad_medida_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.UnidadMedida, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Unidad de Medida modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_UnidadMedida(DeleteView):
    model = models.UnidadMedida
    success_url = reverse_lazy('unidad_medida_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.UnidadMedida, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Unidad de Medida eliminada con éxito")
        return HttpResponseRedirect(success_url)

###TIPOD E OPERAACION
class Form_TipoOperacion(forms.ModelForm):
    class Meta:
        model = models.TipoOperacion
        fields = [
            'nombre',

        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_TipoOperacion(UpdateView):
    model = models.TipoOperacion
    form_class = Form_TipoOperacion
    template_name = ('BodegaApp/tipo_operacion_form.html')
    success_url = reverse_lazy('tipo_operacion_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.TipoOperacion, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Tipo de Operación modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_TipoOperacion(DeleteView):
    model = models.TipoOperacion
    success_url = reverse_lazy('tipo_operacion_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.TipoOperacion, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Tipo de Operación eliminado con éxito")
        return HttpResponseRedirect(success_url)


    ### Producto
class Form_Producto(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = [
            'nombre',
            'codigo',
            # 'precio_costo',
            'precio_venta',
            'unidad',
            'clasificacion',


        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            "codigo": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            # "precio_costo": widgets.NumberInput(attrs={'class': ' form-control', 'required': 'required'}),
            "precio_venta": widgets.NumberInput(attrs={'class': ' form-control', 'required': 'required'}),
            "unidad": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            "clasificacion": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_Producto(UpdateView):
    model = models.Producto
    form_class = Form_Producto
    template_name = ('BodegaApp/producto_form.html')
    success_url = reverse_lazy('producto_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Producto, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Producto modificado con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Producto(DeleteView):
    model = models.Producto
    success_url = reverse_lazy('producto_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Producto, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Producto eliminado con éxito")
        return HttpResponseRedirect(success_url)


    ### BODEGA
class Form_Bodega(forms.ModelForm):
    class Meta:
        model = models.Bodega
        fields = [
            'nombre',
            'admin',
            'zona',
            'productos',


        ]
        widgets = {
            "nombre": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            "admin": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            "zona": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            "productos": widgets.SelectMultiple(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_Bodega(UpdateView):
    model = models.Bodega
    form_class = Form_Bodega
    template_name = ('BodegaApp/bodega_form.html')
    success_url = reverse_lazy('bodega_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Bodega, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Bodega modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Bodega(DeleteView):
    model = models.Bodega
    success_url = reverse_lazy('bodega_listar')

    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Bodega, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Bodega eliminada con éxito")
        return HttpResponseRedirect(success_url)

###NOTIFICACIONES GENERSKES
class Form_NotiGeneral(forms.ModelForm):
    class Meta:
        model = models.Notificacion_general
        fields = [
            'titulo',
            'mensaje',


        ]
        widgets = {
            "titulo": widgets.TextInput(attrs={'class': ' form-control', 'required': 'required'}),
            "mensaje": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

class Update_NotiGeneral(UpdateView):
    model = models.Notificacion_general
    form_class = Form_NotiGeneral
    template_name = ('BodegaApp/notificacion_form.html')
    success_url = reverse_lazy('notificacion_listar')

    def post(self, request, *args, **kwargs):
        register_logs(request, models.Notificacion_general, self.get_object().pk, self.get_object().__str__(), 2)
        # notify.send(request.user , recipient=self.get_object(), verb='Se han modificado sus datos', level='warning')
        self.object = self.get_object()
        messages.success(request, "Notificación modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_NotiGeneral(DeleteView):
    model = models.Notificacion_general
    success_url = reverse_lazy('notificacion_listar')
    template_name = ('BodegaApp/notificacion_confirm_delete.html')


    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Notificacion_general, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Notificación eliminada con éxito")
        return HttpResponseRedirect(success_url)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!OPERACIONES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Form_Operacion(forms.ModelForm):
    class Meta:
        model = models.Operacion
        fields = [
            'bodega',
            'producto',
            'seccion_operacion',
            # 'precio_costo',
            'cantidad',
            'factura',

        ]
        widgets = {
            "bodega": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            "producto": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            "seccion_operacion": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
            # "precio_costo": widgets.NumberInput(attrs={'class': ' form-control', 'required': 'required'}),
            "cantidad": widgets.NumberInput(attrs={'class': ' form-control'}),
            "factura": widgets.TextInput(attrs={'class': ' form-control'}),
            # "total": widgets.NumberInput(attrs={'class': ' form-control'}),
            # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
            # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
            # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
            # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
            # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
        }

        labels ={
            "cantidad": "Cantidad en Libras"
        }


# class Form_Operacion1(forms.ModelForm):
#     class Meta:
#         model = models.Operacion
#         fields = [
#             'bodega',
#             'producto',
#             'seccion_operacion',
#             # 'precio_costo',
#             'cantidad',
#             'factura',
#
#         ]
#         widgets = {
#             "bodega": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
#             "producto": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
#             "seccion_operacion": widgets.Select(attrs={'class': ' form-control', 'required': 'required'}),
#             # "precio_costo": widgets.NumberInput(attrs={'class': ' form-control', 'required': 'required'}),
#             "cantidad": widgets.NumberInput(attrs={'class': ' form-control', }),
#             "factura": widgets.TextInput(attrs={'class': ' form-control'}),
#             # "total": widgets.NumberInput(attrs={'class': ' form-control'}),
#             # "descripcion": widgets.Textarea(attrs={'class': ' form-control', 'required': 'required'}),
#             # "email": widgets.EmailInput(attrs={'class': ' form-control'}),
#             # "groups": widgets.SelectMultiple(attrs={'class': ' form-control'}),
#             # "is_active": widgets.CheckboxInput(attrs={'class': ' form-control'}),
#             # "imagen": widgets.FileInput(attrs={'class': ' form-control'}),
#         }
#         labels ={
#             "cantidad": "Cantidad en Kilogramos"
#         }


class Update_Operacion(UpdateView):
    model = models.Operacion
    form_class = Form_Operacion
    template_name = ('BodegaApp/operacion_form.html')
    success_url = reverse_lazy('operacion_listar')


    def post(self, request, *args, **kwargs):
        register_logs(request, models.Operacion, self.get_object().pk, self.get_object().__str__(), 2)
        messages.success(request, "Operación modificada con éxito")
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

class Delete_Operacion(DeleteView):
    model = models.Operacion
    success_url = reverse_lazy('operacion_listar')
    template_name = ('BodegaApp/operacion_confirm_delete.html')


    def delete(self, request, *args, **kwargs):
        register_logs(request, models.Operacion, self.get_object().pk, self.get_object().__str__(), 3)
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Operación eliminada con éxito")
        return HttpResponseRedirect(success_url)