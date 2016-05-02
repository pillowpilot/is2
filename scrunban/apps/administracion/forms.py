from django import forms
from django.core.exceptions import ValidationError
from apps.autenticacion.models import User

class ProjectForm(forms.Form):
    name = forms.CharField(label = "Nombre del Proyecto", max_length=128)
    date_start = forms.DateField(label = "Fecha de inicio")
    date_end = forms.DateField(label = "Fecha de finalizacion")
    scrum_master = forms.CharField(label = "Scrum Master", max_length = 128)
    product_owner = forms.CharField(label = "Product Owner", max_length = 128)


class UserForm(forms.Form):
    id = forms.CharField(max_length=4,widget=forms.HiddenInput, required=False)
    username = forms.CharField(max_length=128,widget=forms.HiddenInput, required=False)
    password = forms.CharField(max_length=128,widget=forms.HiddenInput, required=False)
    first_name = forms.CharField(max_length=128, widget=forms.HiddenInput, required=False)
    last_name = forms.CharField(max_length=128, widget=forms.HiddenInput, required=False)
    direccion = forms.CharField(max_length=128, widget=forms.HiddenInput, required=False)
    telefono = forms.CharField(max_length=128, widget=forms.HiddenInput, required=False)
    email = forms.CharField(max_length=128, widget=forms.HiddenInput, required=False)

    def clean_username(self):
        if not(self.cleaned_data['username'] == ''):
            if not(self.cleaned_data['username'].isdigit()):
                raise ValidationError('Este campo solo puede contener numeros')

        return self.cleaned_data['username']

class UserCreateForm(UserForm):

    username = forms.CharField(max_length=128, required=True, widget=forms.HiddenInput)
    password = forms.CharField(max_length=128, required=True, widget=forms.HiddenInput)

    def clean_username(self):

        if len(User.users.filter(username=self.cleaned_data['username'])) != 0:
            raise ValidationError('El usuario ya existe')

        return self.cleaned_data['username']

    def save(self):

        data = {
            'username' : self.cleaned_data['username'],
            'password' : self.cleaned_data['password'],
            'direccion' : self.cleaned_data.get('direccion', ''),
            'email': self.cleaned_data.get('email', ''),
            'telefono': self.cleaned_data.get('telefono', ''),
            'first_name': self.cleaned_data.get('first_name', ''),
            'last_name': self.cleaned_data.get('last_name', '')
        }


        User.users.create(**data)


class UserEditForm(UserForm):
    id = forms.CharField(max_length=4, required=True, widget=forms.HiddenInput)

    def clean_id(self):
        if len(User.objects.filter(id=self.cleaned_data['id'])):
            raise ValidationError('El usuario especificado no existe')
        return self.cleaned_data['id']

    def save(self):
        data = {
            'email': self.cleaned_data.get('email', ''),
            'first_name': self.cleaned_data.get('first_name', ''),
            'last_name': self.cleaned_data.get('last_name', ''),
            'direccion': self.cleaned_data.get('direccion', ''),
            'telefono': self.cleaned_data.get('telefono', ''),
        }

        user = User.objects.filter(id=self.cleaned_data['id'])[0]

        if (data['email'] != ''):
            user.set_email(data['email'])

        if (data['first_name'] != ''):
            user.set_first_name(data['first_name'])

        if (data['last_name'] != ''):
            user.set_last_name(data['last_name'])

        if (data['direccion'] != ''):
            user.set_direccion(data['direccion'])

        if (data['telefono'] != ''):
            user.set_telefono(data['telefono'])

        user.save()


class UserDeleteForm(UserForm):
    id = forms.CharField(max_length=4, required=True, widget=forms.HiddenInput)

    def clean_id(self):

        if len(User.objects.filter(id=self.cleaned_data['id'])) == 0:
            raise ValidationError('El usuario especificado no existe')
        return self.cleaned_data['id']


    def save(self):
        u = User.objects.filter(id=self.cleaned_data['id'])[0]
        u.delete()
