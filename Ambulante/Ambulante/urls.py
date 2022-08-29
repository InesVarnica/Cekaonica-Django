"""Ambulante URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from django.contrib import admin
from django.urls import path
from App import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('index/', views.index, name='index'),
    path('lista_korisnika/', views.lista_korisnika, name='lista_korisnika'),
    path('unos_korisnika/', views.unos_korisnika, name='unos_korisnika'),
    path('lista_radilista/', views.lista_radilista, name='lista_radilista'),
    path('unos_radilista/', views.unos_radilista, name='unos_radilista'),
    path('lista_utrosaka/', views.lista_utrosaka, name='lista_utrosaka'),
    path('unos_utroska/', views.unos_utroska, name='unos_utroska'),
    path('lista_pacijenata/', views.lista_pacijenata, name='lista_pacijenata'),
    path('unos_pacijenata/<int:radilište_id>', views.unos_pacijenata, name='unos_pacijenata'),
    path('blagajna/', views.blagajna, name='blagajna'),
    path('korisnik_radilište/<int:korisnik_id>', views.korisnik_radilište, name='korisnik_radilište'),
    path('ažuriraj_korisnika/<int:zaposlenik_id>', views.ažuriraj_korisnika, name='ažuriraj_korisnika'),
    path('ažuriraj_pacijenta/<int:pacijent_id>', views.ažuriraj_pacijenta, name='ažuriraj_pacijenta'),
    path('password/<int:zaposlenik_id>', views.change_password_zaposlenik, name='password'),
    path('profil_pacijent/<int:pacijent_id>', views.profil_pacijent, name='profil_pacijent'),
    path('lista_korisnikovih_radilista/<int:zaposlenik_id>', views.lista_korisnikovih_radilista, name='lista_korisnikovih_radilista'),
    path('sestrinska_čekaonica/<int:radilište_id>', views.sestrinska_čekaonica, name='sestrinska_čekaonica'),
    path('pretraži_pacijenta/<int:radilište_id>', views.pretraži_pacijenta, name='pretraži_pacijenta'),
    path('posjeta/<int:radilište_id>/<int:pacijent_id>', views.posjeta, name='posjeta'),
    path('utrošak_posjeta/<int:posjeta_id>', views.unesi_utrošak_za_posjetu, name='utrošak_posjeta'),
    path('naplata/<int:posjeta_id>', views.naplata, name='naplata'),
    path('posjeta/<int:radilište_id>/<int:pacijent_id>', views.posjeta, name='posjeta'),
    path('nalaz/<int:posjeta_id>/', views.nalaz, name='nalaz'),
    path('otpust/<int:posjeta_id>/', views.otpust, name='otpust'),
    path('arhiva/<int:pacijent_id>/<int:posjeta_id>/', views.arhiva, name='arhiva'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('search_pacijent', views.search_pacijent, name='search_pacijent'),
    path('search_korisnik', views.search_zaposlenik, name='search_korisnik'),
    path('search_radilište', views.search_radilište, name='search_radilište'),
    path('search_utrošak', views.search_utrošak, name='search_utrošak'),
    path('nalaz_pdf/<int:nalaz_id>', views.nalaz_pdf, name='nalaz_pdf'),

    
]