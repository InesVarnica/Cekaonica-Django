from errno import EMLINK
from wsgiref.validate import validator
from .models import Korisnik, Nalaz, RegistarPacijenata, Uputnice, Radilišta, Posjeta, ŠifrarnikUtrošak, Utrošak_posjeta
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import ModelForm
from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator,MaxValueValidator
from crispy_forms.helper import FormHelper
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import (PasswordResetForm, SetPasswordForm)
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.utils.safestring import mark_safe
from crispy_forms.layout import Layout, ButtonHolder, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText


class AddUserForm(UserCreationForm):  

    class Meta:
        model = Korisnik
        fields = ['first_name','last_name','username','email','role']

    def __init__(self, *args, **kwargs):
            super(AddUserForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.fields['first_name'].label = ""
            self.fields['last_name'].label = ""
            self.fields['username'].label = ""
            self.fields['email'].label = ""
            self.fields['role'].label = ""


class SetPasswordForm(SetPasswordForm):  


    _placeholders = {
        'new_password1': 'new_password1 placeholder',
    }

    def __init__(self, *args, **kwargs):
            super(SetPasswordForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.fields['new_password1'].label = "Lozinka"
            self.fields['new_password2'].label = "Ponovi lozinku"

            self.helper.layout = Layout(
            PrependedText('new_password1', '@', placeholder="username"),
        )
    
    

class editUserForm(UserChangeForm):  
    

    class Meta:
        model = Korisnik
        fields = ['first_name','last_name','username','email','role']

    def __init__(self, *args, **kwargs):
            super(editUserForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_show_labels = False
            self.fields['first_name'].label = ""
            self.fields['last_name'].label = ""
            self.fields['username'].label = ""
            self.fields['email'].label = ""
            self.fields['role'].label = ""
            self.fields['password'].label = ""



class AddRadilištaForm(ModelForm):

    class Meta:

        model = Radilišta
        fields = ['klinika','naziv',]

class AddPacijentForm(ModelForm):

    class Meta:

        model = RegistarPacijenata
        fields = ['MBO','ime','prezime', 'datum_rođenja','email','broj_telefona','adresa','status_osiguranja','datum_police_osiguranja']


class PretražiPacijentaForm(forms.Form):


    MBO = forms.IntegerField(required=False)
    Ime = forms.CharField(required=False)
    Prezime = forms.CharField(required=False)
    Datum_rođenja=forms.DateField(required=False)


class CustomModelFilter(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

class PosjetaForm(ModelForm):

    zaposlenik = CustomModelFilter(queryset=Korisnik.objects.filter(role='spec').filter())

    
    class Meta:

        model = Posjeta
        fields = ['zaposlenik','uputnica']

    
class ŠifrarnikUtrošakForm(ModelForm):

    class Meta:

        model = ŠifrarnikUtrošak
        fields = ['šifra','naziv','cijena']


class PosjetaUtrošakForm(ModelForm):


   class Meta:

        model = Utrošak_posjeta
        fields = ['utrošak','količina_utroška']


class CustomModelFilter(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)


class NalazForm(ModelForm):

    zaposlenik = CustomModelFilter(queryset=Korisnik.objects.filter(role='spec').filter())
    zaposlenik2 = CustomModelFilter(queryset=Korisnik.objects.filter(role='dr').filter())
    
    class Meta:

        model = Nalaz
        fields = ['dijagnoza','razlog_dolaska','anamneza','terapija','zaključak','zaposlenik','zaposlenik2']

class OtpustForm(ModelForm):

    class Meta:

        model = Posjeta
        fields = ['status_otpusta', ]