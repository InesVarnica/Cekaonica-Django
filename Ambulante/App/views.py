from datetime import date
from mailbox import linesep
from os import curdir
from re import U
from tkinter import N
from tokenize import blank_re
from turtle import pos
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, HttpResponseRedirect
from .models import Korisnik, Nalaz, Posjeta, RegistarPacijenata, Uputnice, Radilišta, Radilište_korisnik, Utrošak_posjeta, ŠifrarnikUtrošak,Blagajna
from .forms import PosjetaForm, AddRadilištaForm, AddUserForm, AddPacijentForm, PosjetaUtrošakForm, PretražiPacijentaForm, ŠifrarnikUtrošakForm, NalazForm, OtpustForm, editUserForm,SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import datetime
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



@login_required
def index(request):
    current_user = request.user
    print(current_user)
    print(current_user.role)
    if current_user.is_superuser:
        return render(request, 'index.html',{'user':current_user})
    elif current_user.role == 'ms' or 'vms' or 'spec' or 'dr':
        return(redirect('lista_korisnikovih_radilista' , zaposlenik_id = current_user.id))



@login_required
def unos_radilista(request):  
    if request.method == 'GET':
        RegisterForm = AddRadilištaForm()
        return render(request, 'unos_radilista.html',{'form':RegisterForm })   
    else:  
        RegisterForm = AddRadilištaForm(request.POST)
        if RegisterForm.is_valid():
            uneseni_naziv = RegisterForm.cleaned_data.get('naziv')
            uneseni_klinika = RegisterForm.cleaned_data.get('klinika')
            radilište=Radilišta.objects.filter(naziv=uneseni_naziv).filter(klinika=uneseni_klinika)
            if(radilište):
                messages.error(request,'Radilište već postoji')
                return redirect('unos_radilista')
            else:
                RegisterForm.save()
                messages.error(request,'Radilište uspješno dodano')
                return redirect('unos_radilista')  
    return HttpResponse("Something went wrong!")


@login_required
def unos_korisnika(request):  
    if request.method == 'GET':
        UserForm = AddUserForm()
        return render(request, 'unos_korisnika.html',{'form':UserForm })   
    else:  
        UserForm = AddUserForm(request.POST)
        if UserForm.is_valid():
            uneseni_email = UserForm.cleaned_data.get('email')
            username = UserForm.cleaned_data.get('username')
            korisnik_email=Korisnik.objects.filter(email=uneseni_email)
            korisnik_username=Korisnik.objects.filter(username=username)
            if(korisnik_email ):
                messages.error(request,'Email je zauzet')
                return redirect('unos_korisnika')
            else:
                UserForm.save()
                messages.error(request,'Korisnik uspješno dodan')
                return redirect('unos_korisnika') 
        else:
            messages.error(request,'Niste ispravno unijeli podatke') 
            return redirect('unos_korisnika') 
    
@login_required
def lista_korisnika(request):
    
    p = Paginator(Korisnik.objects.all(), 6)
    page = request.GET.get('page')
    korisnici = p.get_page(page)
    return render(request, 'lista_korisnika.html',{"data":korisnici})

@login_required
def korisnik_radilište(request,korisnik_id):

    zaposlenik_u=Korisnik.objects.get(id=korisnik_id)
    if 'nedodani' in request.POST:
        q=(request.POST)
        radilište_u=Radilišta.objects.get(pk=q['nedodani'])
        dodana_radilišta=Radilište_korisnik(radilište=radilište_u, zaposlenik=zaposlenik_u)
        dodana_radilišta.save()

    if 'dodana' in request.POST:
        q=(request.POST)
        #upisano_radilište=Radilište_korisnik.objects.filter(zaposlenik=korisnik_id)
        upisano_radilište=Radilište_korisnik.objects.filter(zaposlenik=korisnik_id).get(radilište=q['dodana'])
        upisano_radilište.delete()

    #upisani#
    
    upisana_radilišta = Radilište_korisnik.objects.all().filter(zaposlenik=korisnik_id)
    upisani_radilišta_id = list(upisana_radilišta.values_list('radilište_id', flat=True))
    

    #neupisani#

    radilišta_id = []
    radilišta=Radilišta.objects.all()
    radilišta_id = list(radilišta.values_list('id', flat=True))
    neupisani_radilišta_id=set(radilišta_id)-set(upisani_radilišta_id)
    
    neupisana_radilišta = []
    for id in neupisani_radilišta_id:
        neupisana_radilišta.append(Radilišta.objects.get(pk=id))
    
    p = Paginator(neupisana_radilišta, 5)
    page = request.GET.get('page')
    neupisana_radilišta = p.get_page(page)

    p = Paginator(upisana_radilišta, 5)
    page = request.GET.get('page')
    upisana_radilišta = p.get_page(page)

    return render(request, 'korisnik_radiliste.html',{'upisana_radilišta':upisana_radilišta, 'neupisana_radilišta':neupisana_radilišta, 'zaposlenik':zaposlenik_u})

@login_required
def lista_radilista(request):
    p = Paginator(Radilišta.objects.all().order_by('klinika'), 6)
    page = request.GET.get('page')
    radilišta = p.get_page(page)
    return render(request, 'lista_radilista.html',{"radilišta":radilišta})

@login_required
def lista_pacijenata(request):
    p = Paginator(RegistarPacijenata.objects.all().order_by('ime'), 6)
    page = request.GET.get('page')
    pacijenti = p.get_page(page)
    return render(request, 'lista_pacijenata.html',{"pacijenti":pacijenti})

@login_required
def lista_utrosaka(request):
    p = Paginator(ŠifrarnikUtrošak.objects.all().order_by('šifra'), 6)
    page = request.GET.get('page')
    utrosci = p.get_page(page)
    return render(request, 'lista_utrosaka.html',{"utrošci":utrosci})


@login_required
def lista_korisnikovih_radilista(request,zaposlenik_id):
    current_user = request.user
    radilišta=Radilište_korisnik.objects.filter(zaposlenik=zaposlenik_id)
 
    return render(request, 'lista_korisnikovih_radilista.html',{"radilišta":radilišta, "user":current_user})


@login_required
def unos_pacijenata(request,radilište_id):  
    current_user = request.user
    if request.method == 'GET':
        UserForm = AddPacijentForm()
        return render(request, 'unos_pacijenata_registar.html',{'form':UserForm })   
    else:  
        UserForm = AddPacijentForm(request.POST)
        if UserForm.is_valid():
            uneseni_MBO = UserForm.cleaned_data.get('MBO')
            if uneseni_MBO:
                try:
                    korisnik_MBO=RegistarPacijenata.objects.get(MBO=uneseni_MBO)
                except RegistarPacijenata.DoesNotExist:
                    korisnik_MBO = None
                if korisnik_MBO != None:
                    messages.error(request,'Korisnik s tim MBO-om postoji')
                    return redirect('unos_pacijenata')  
                elif uneseni_MBO == None:
                    if(uneseni_MBO > 999999999  or uneseni_MBO < 100000000):
                        messages.error(request,'MBO je prevelik ili premali')
                        return redirect('unos_pacijenata')
                else:
                    UserForm.save()
                    messages.error(request,'Korisnik uspješno dodan')
                    UserForm.save()
                    messages.error(request,'Korisnik uspješno dodan')
                    if current_user.role == 'ms' or current_user.role == 'vms' or current_user.role == 'dr' or current_user.role == 'spec' :
                        return redirect('sestrinska_čekaonica',radilište_id = radilište_id)
                    else:
                        return redirect('unos_pacijenata', radilište_id = radilište_id)
                    
            else:
                UserForm.save()
                messages.error(request,'Korisnik uspješno dodan')
                if current_user.role == 'ms' or current_user.role == 'vms' or current_user.role == 'dr' or current_user.role == 'spec' :
                    return redirect('sestrinska_čekaonica', radilište_id = radilište_id)
                else:
                    return redirect('unos_pacijenata', radilište_id = radilište_id)
                    
        else:
            messages.error(request,'Krivi unos podataka') 
            return redirect('unos_pacijenata', radilište_id = radilište_id) 

@login_required
def pretraži_pacijenta(request, radilište_id):  
    if request.method == 'GET':
        UserForm = PretražiPacijentaForm()
        return render(request, 'pretraži_pacijenta.html',{'form':UserForm , "radilište_id":radilište_id})   
    else:  
        UserForm = PretražiPacijentaForm(request.POST)
        if UserForm.is_valid():
            uneseni_MBO = UserForm.cleaned_data['MBO']
            uneseno_ime = UserForm.cleaned_data['Ime']
            uneseno_prezime = UserForm.cleaned_data['Prezime']
            uneseni_datum_rođenja = UserForm.cleaned_data['Datum_rođenja']
            
            if uneseni_MBO and uneseno_ime and uneseno_prezime and uneseni_datum_rođenja:
                pacijent = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(ime=uneseno_ime).filter(MBO=uneseni_MBO).filter(datum_rođenja=uneseni_datum_rođenja)
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik":pacijent, 'radilište':radilište_id})

            elif uneseni_MBO and uneseno_ime and uneseno_prezime or uneseni_datum_rođenja and uneseno_ime and uneseno_prezime or uneseni_MBO and uneseni_datum_rođenja and uneseno_prezime or uneseni_MBO and uneseno_ime and uneseni_datum_rođenja:
                pacijent1 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(ime=uneseno_ime).filter(datum_rođenja=uneseni_datum_rođenja)
                pacijent2 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(MBO=uneseni_MBO).filter(datum_rođenja=uneseni_datum_rođenja)
                pacijent3 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(ime=uneseno_ime).filter(datum_rođenja=uneseni_datum_rođenja)
                pacijent4 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(ime=uneseno_ime).filter(prezime=uneseno_prezime)
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik1":pacijent1,"korisnik2":pacijent2,"korisnik3":pacijent3,"korisnik4":pacijent4 , 'radilište':radilište_id})

            elif uneseni_MBO and uneseno_ime or uneseno_prezime and uneseno_ime or uneseno_prezime and uneseni_MBO or uneseni_datum_rođenja and uneseni_MBO or uneseni_datum_rođenja and uneseno_ime or uneseni_datum_rođenja and uneseno_prezime or uneseni_datum_rođenja: 
                pacijent1 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(ime=uneseno_ime)
                if uneseni_MBO != None:
                    pacijent2 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(MBO=uneseni_MBO)
                    pacijent3 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(ime=uneseno_ime)
                    pacijent4 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(datum_rođenja=uneseni_datum_rođenja)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik3":pacijent3,"korisnik4":pacijent4 ,"korisnik2":pacijent2,'radilište':radilište_id})
                if uneseni_datum_rođenja != None:
                    pacijent5 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(datum_rođenja=uneseni_datum_rođenja)
                    pacijent6 = RegistarPacijenata.objects.all().filter(ime=uneseno_ime).filter(datum_rođenja=uneseni_datum_rođenja)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik5":pacijent5,"korisnik6":pacijent6,'radilište':radilište_id})
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik1":pacijent1,'radilište':radilište_id})

            elif uneseni_MBO or uneseno_ime or uneseno_prezime or uneseni_datum_rođenja:
                pacijent1 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime)
                if uneseni_MBO != None:
                    pacijent2 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik2":pacijent2 ,'radilište':radilište_id})
                pacijent3 = RegistarPacijenata.objects.all().filter(ime=uneseno_ime)
                if  uneseni_datum_rođenja != None:
                    pacijent4 = RegistarPacijenata.objects.all().filter(datum_rođenja=uneseni_datum_rođenja)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik4":pacijent4, 'radilište':radilište_id})
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik1":pacijent1,"korisnik3":pacijent3, 'radilište':radilište_id})
            
        else:
            return redirect('pretraži_pacijenta') 

def posjeta(request,radilište_id, pacijent_id):
    if request.method == 'GET':
        Form = PosjetaForm()
        return render(request, 'posjeta.html',{'form':Form , "radilište_id":radilište_id}) 
    else:
        radilište=Radilišta.objects.get(pk=radilište_id)
        print(radilište)
        pacijent_u=RegistarPacijenata.objects.get(pk=pacijent_id) 
        print(pacijent_u)
        Form = PosjetaForm(request.POST)
        if Form.is_valid():
            zaposlenik_u = Form.cleaned_data.get('zaposlenik')
            uputnica_u = Form.cleaned_data.get('uputnica')
            posjeta = Posjeta(pacijent=pacijent_u,naziv_radilišta=radilište,zaposlenik=zaposlenik_u,uputnica=uputnica_u)
            posjeta.save()
            return(redirect('sestrinska_čekaonica' , radilište_id = radilište_id))
        else:
            messages.error(request,'Nešto je pošlo po zlu') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def pretraži_pacijenta_registar(request): 
    current_user = request.user
    if request.method == 'GET':
        UserForm = PretražiPacijentaForm()
        return render(request, 'pretraži_pacijenta_registar.html',{'form':UserForm})   
    else:  
        UserForm = PretražiPacijentaForm(request.POST)
        if UserForm.is_valid():
            uneseni_MBO = UserForm.cleaned_data['MBO']
            uneseno_ime = UserForm.cleaned_data['Ime']
            uneseno_prezime = UserForm.cleaned_data['Prezime']
            uneseni_datum_rođenja = UserForm.cleaned_data['Datum_rođenja']
                        
            if uneseni_MBO and uneseno_ime and uneseno_prezime and uneseni_datum_rođenja:
                pacijent = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(ime=uneseno_ime).filter(MBO=uneseni_MBO).filter(datum_rođenja=uneseni_datum_rođenja)
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik":pacijent})

            elif uneseni_MBO and uneseno_ime and uneseno_prezime or uneseni_datum_rođenja and uneseno_ime and uneseno_prezime or uneseni_MBO and uneseni_datum_rođenja and uneseno_prezime or uneseni_MBO and uneseno_ime and uneseni_datum_rođenja:
                pacijent1 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(ime=uneseno_ime).filter(datum_rođenja=uneseni_datum_rođenja)
                pacijent2 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(MBO=uneseni_MBO).filter(datum_rođenja=uneseni_datum_rođenja)
                pacijent3 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(ime=uneseno_ime).filter(datum_rođenja=uneseni_datum_rođenja)
                pacijent4 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(ime=uneseno_ime).filter(prezime=uneseno_prezime)
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik1":pacijent1,"korisnik2":pacijent2,"korisnik3":pacijent3,"korisnik4":pacijent4})

            elif uneseni_MBO and uneseno_ime or uneseno_prezime and uneseno_ime or uneseno_prezime and uneseni_MBO or uneseni_datum_rođenja and uneseni_MBO or uneseni_datum_rođenja and uneseno_ime or uneseni_datum_rođenja and uneseno_prezime or uneseni_datum_rođenja: 
                pacijent1 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(ime=uneseno_ime)
                if uneseni_MBO != None:
                    pacijent2 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(MBO=uneseni_MBO)
                    pacijent3 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(ime=uneseno_ime)
                    pacijent4 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO).filter(datum_rođenja=uneseni_datum_rođenja)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik3":pacijent3,"korisnik4":pacijent4 ,"korisnik2":pacijent2})
                if uneseni_datum_rođenja != None:
                    pacijent5 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime).filter(datum_rođenja=uneseni_datum_rođenja)
                    pacijent6 = RegistarPacijenata.objects.all().filter(ime=uneseno_ime).filter(datum_rođenja=uneseni_datum_rođenja)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik5":pacijent5,"korisnik6":pacijent6})
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik1":pacijent1})

            elif uneseni_MBO or uneseno_ime or uneseno_prezime or uneseni_datum_rođenja:
                pacijent1 = RegistarPacijenata.objects.all().filter(prezime=uneseno_prezime)
                if uneseni_MBO != None:
                    pacijent2 = RegistarPacijenata.objects.all().filter(MBO=uneseni_MBO)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik2":pacijent2})
                pacijent3 = RegistarPacijenata.objects.all().filter(ime=uneseno_ime)
                if  uneseni_datum_rođenja != None:
                    pacijent4 = RegistarPacijenata.objects.all().filter(datum_rođenja=uneseni_datum_rođenja)
                    return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik4":pacijent4})
                return render(request, 'lista_pretraženih_pacijenata.html',{"korisnik1":pacijent1,"korisnik3":pacijent3})
            
        else:
            messages.error(request,'Krivi unos,datum rođenja mora imati format GGGG-MM-DD') 
            return redirect('pretraži_pacijenta')

def unos_utroska(request):
    if request.method == 'GET':
        RegisterForm = ŠifrarnikUtrošakForm()
        return render(request, 'unos_utroška.html',{'form':RegisterForm })   
    else:  
        RegisterForm = ŠifrarnikUtrošakForm(request.POST)
        if RegisterForm.is_valid():
            uneseni_naziv = RegisterForm.cleaned_data.get('naziv')
            unesena_šifra = RegisterForm.cleaned_data.get('šifra')
            utrošak_naziv=ŠifrarnikUtrošak.objects.filter(naziv=uneseni_naziv)
            utrošak_šifra=ŠifrarnikUtrošak.objects.filter(šifra=unesena_šifra)
            if(utrošak_naziv or utrošak_šifra):
                messages.error(request,'Utrošak već postoji')
                return redirect('unos_utroska')
            else:
                RegisterForm.save()
                messages.error(request,'Utrošak uspješno dodano')
                return redirect('unos_utroska')  
    return HttpResponse("Something went wrong!")


def sestrinska_čekaonica(request,radilište_id):
    radilište=Radilišta.objects.get(pk=radilište_id)
    date=datetime.datetime.now().date()
    print(date)
    nalazi=[]
    nalazi2=[]
    current_user = request.user
    pacijenti=Posjeta.objects.all().filter(naziv_radilišta__id=radilište_id)

    if 'obrisi' in request.POST:
        q=(request.POST)
        posjeta=Posjeta.objects.get(pk=q['obrisi'])
        posjeta.delete()

    for p in pacijenti:
        try:
            posjeta=Nalaz.objects.get(posjeta=p)
            nalazi.append(posjeta)
        except Nalaz.DoesNotExist:
            nalazi2.append(p)
    return render(request, 'sestrinska_čekaonica.html',{'pacijenti':nalazi2,'radilište':radilište, 'user':current_user,'nalazi':nalazi ,'date':date})

def unesi_utrošak_za_posjetu(request,posjeta_id):
    utrošak_posjete=Utrošak_posjeta.objects.all().filter(posjeta=posjeta_id)
    posjeta=Posjeta.objects.get(pk=posjeta_id)
    radilište_id=posjeta.naziv_radilišta.id
    try:
        naplata=Blagajna.objects.get(posjeta=posjeta_id)
    except Blagajna.DoesNotExist:
        naplata = None
    if naplata == None:
        if request.method == 'GET':
            Form = PosjetaUtrošakForm()
            return render(request, 'utrošak_posjeta.html',{'form':Form , 'utrošak_posjete':utrošak_posjete, 'posjeta':posjeta,'radilište_id':radilište_id}) 
        else:  
            Form = PosjetaUtrošakForm(request.POST)
            
            if Form.is_valid():
                uneseni_utrošak = Form.cleaned_data.get('utrošak')
                unesena_količina = Form.cleaned_data.get('količina_utroška')
                if(uneseni_utrošak and unesena_količina):
                    try:
                        utrošak=Utrošak_posjeta.objects.filter(utrošak=uneseni_utrošak).get(posjeta=posjeta_id)
                    except Utrošak_posjeta.DoesNotExist:
                        utrošak = None
                    if utrošak==None:
                        utrošak_posjeta = Utrošak_posjeta(utrošak=uneseni_utrošak,količina_utroška=unesena_količina,posjeta=posjeta)
                        utrošak_posjeta.save()
                    else:
                        utrošak=Utrošak_posjeta.objects.filter(utrošak=uneseni_utrošak).get(posjeta=posjeta_id)
                        količina=utrošak.količina_utroška
                        nova_količina=količina+1
                        utrošak.količina_utroška=nova_količina
                        utrošak.save()
                        
                    return render(request, 'utrošak_posjeta.html',{'form':Form , 'utrošak_posjete':utrošak_posjete, 'posjeta':posjeta,'radilište_id':radilište_id}) 
                elif 'Delete' in request.POST:
                    print('nesto')
                    q=(request.POST)
                    print(q['Delete'])
                    utrošak=Utrošak_posjeta.objects.filter(posjeta=posjeta_id).get(utrošak=q['Delete'])
                    print(utrošak)
                    količina=utrošak.količina_utroška
                    if količina == 1:
                        utrošak.delete()
                    else:
                        nova_količina=količina-1
                        utrošak.količina_utroška=nova_količina
                        utrošak.save()
                    return render(request, 'utrošak_posjeta.html',{'form':Form , 'utrošak_posjete':utrošak_posjete, 'posjeta':posjeta,'radilište_id':radilište_id}) 

                else:
                    messages.error(request,'Niste ništa dodali')
                    return HttpResponse("Something went wrong!")
            messages.error(request,'Niste ništa dodali')
    else:
        return(redirect('naplata' , posjeta_id = posjeta_id))
    return HttpResponse("Something went wrong!")
    
def naplata(request,posjeta_id):
    posjeta=Posjeta.objects.get(pk=posjeta_id)
    radilište_id=posjeta.naziv_radilišta.id
    ukupno=0
    utrošak=Utrošak_posjeta.objects.all().filter(posjeta=posjeta_id)
    try:
        naplata=Blagajna.objects.get(posjeta=posjeta_id)
    except Blagajna.DoesNotExist:
        naplata = None
    if naplata == None:
        if request.method == 'GET':
            for i in utrošak:
                ukupno+=(i.količina_utroška*i.utrošak.cijena)
            return render(request, 'naplata.html',{'utrošak':utrošak,'ukupno':ukupno,'radilište_id':radilište_id})
        elif 'naplata' in request.POST:
            q=(request.POST)
            ukupno=q['naplata']
            current_user = request.user
            try:
                naplata=Blagajna.objects.get(posjeta=posjeta)
            except Blagajna.DoesNotExist:
                naplata = None
            if naplata == None:
                blagajna = Blagajna(zaposlenik=current_user,cijena=ukupno,posjeta=posjeta)
                blagajna.save()
            else:
                naplata=Blagajna.objects.get(posjeta=posjeta)
                naplata.cijena=ukupno
                naplata.save()
            return(redirect('sestrinska_čekaonica' , radilište_id = radilište_id))
        else:
            return HttpResponse("Something went wrong!")
    else:
        if 'storno' in request.POST:
            naplata=Blagajna.objects.get(posjeta=posjeta)
            naplata.delete()
            return(redirect('utrošak_posjeta' , posjeta_id = posjeta_id))
            
        return render(request, 'naplata.html',{'utrošak':utrošak,'ukupno':ukupno, 'naplata':naplata,'radilište_id':radilište_id})


def blagajna(request):
    blagajna=Blagajna.objects.all()
    ukupno=0
    for naplata in blagajna:
        ukupno+=naplata.cijena
    print(ukupno)
    return render(request, 'blagajna.html',{'blagajna':blagajna,'ukupno':ukupno})



def nalaz(request,posjeta_id):
    current_user = request.user
    posjeta=Posjeta.objects.get(pk=posjeta_id)
    pacijent=posjeta.pacijent
    pacijent_id=posjeta.pacijent.id
    radilište=posjeta.naziv_radilišta
    radilište_id=posjeta.naziv_radilišta.id
    try:
        nalaz=Nalaz.objects.get(posjeta=posjeta_id)
    except Nalaz.DoesNotExist:
        nalaz = None
  
    if nalaz == None:
        if request.method == 'GET':
            Form = NalazForm()
            return render(request, 'nalaz.html',{'form':Form , 'nalaz':nalaz,'posjeta_id':posjeta_id,'pacijent_id':pacijent_id,'pacijent':pacijent,'user':current_user})
        else:  
            Form = NalazForm(request.POST)
            if Form.is_valid():
                dijagnoza = Form.cleaned_data.get('dijagnoza')
                razlog_dolaska = Form.cleaned_data.get('razlog_dolaska')
                anamneza = Form.cleaned_data.get('anamneza')
                zaključak = Form.cleaned_data.get('zaključak')
                terapija = Form.cleaned_data.get('terapija')
                zaposlenik = Form.cleaned_data.get('zaposlenik')
                zaposlenik2 = Form.cleaned_data.get('zaposlenik2')
                nalaz = Nalaz(naziv_nalaza='Specijalistički nalaz',dijagnoza=dijagnoza,posjeta=posjeta,razlog_dolaska=razlog_dolaska,anamneza=anamneza,terapija=terapija,zaključak=zaključak,naziv_radilišta=radilište,zaposlenik=zaposlenik,zaposlenik2=zaposlenik2)
                nalaz.save()
                return(redirect('sestrinska_čekaonica' , radilište_id = radilište_id,))
    else:
        nalaz=Nalaz.objects.get(posjeta=posjeta_id)
        if request.method == 'GET':
            Form = NalazForm(instance=nalaz)
            return render(request, 'nalaz.html',{'form':Form , 'nalaz':nalaz ,'posjeta_id':posjeta_id,'pacijent_id':pacijent_id,'pacijent':pacijent,'user':current_user})
        else:
            if 'ažuriraj' in request.POST:
                data_to_update = NalazForm(request.POST, instance=nalaz)
                if data_to_update.is_valid():
                    data_to_update.save()
                return(redirect('sestrinska_čekaonica' , radilište_id = radilište_id))
            else:
                nalaz.delete()
                return(redirect('sestrinska_čekaonica' , radilište_id = radilište_id))
    return HttpResponse("Something went wrong!")

   
def otpust(request, posjeta_id):
    posjeta=Posjeta.objects.get(pk=posjeta_id)
    pacijent_id=posjeta.pacijent.id
    pacijent=posjeta.pacijent
    radilište=posjeta.naziv_radilišta
    radilište_id=posjeta.naziv_radilišta.id
    date= datetime.datetime.now()
    if request.method == 'GET':
        Form = OtpustForm()
        return render(request, 'otpust.html',{'form':Form,'posjeta_id':posjeta_id,'pacijent_id':pacijent_id,'pacijent':pacijent,'posjeta':posjeta,'date':date})
    else:  
        Form = OtpustForm(request.POST)
        if Form.is_valid():
            data_to_update = OtpustForm(request.POST, instance=posjeta)
            data_to_update.save()
            posjeta.vrijeme_otpusta = datetime.datetime.now()
            print(datetime.datetime)
            posjeta.save()
            return(redirect('sestrinska_čekaonica' , radilište_id = radilište_id))
       
    return HttpResponse("Something went wrong!")
            
def arhiva(request,pacijent_id,posjeta_id):
    nalaz=[]
    pacijent=RegistarPacijenata.objects.get(pk=pacijent_id)
    posjete=Posjeta.objects.all().filter(pacijent=pacijent)
  
    for posjeta in posjete:
        try:
            nalaz.append(Nalaz.objects.filter(posjeta=posjeta).get())
        except Nalaz.DoesNotExist:
            pass
    print(nalaz)
    for n in nalaz:
        print(n)
    return render(request, 'arhiva.html',{'nalazi':nalaz,'pacijent_id':pacijent_id ,'posjeta_id':posjeta_id,'pacijent':pacijent})


@login_required
def profil_pacijent(request,pacijent_id):
    current_user = request.user
    pacijent=RegistarPacijenata.objects.get(pk=pacijent_id)
    p = Paginator(Posjeta.objects.all().filter(pacijent=pacijent), 5)
    page = request.GET.get('page')
    posjete = p.get_page(page)
    return render(request, 'pacijent_profil.html',{'pacijent':pacijent,'posjete':posjete,'user':current_user })

@login_required
def ažuriraj_korisnika(request,zaposlenik_id):
    zaposlenik=Korisnik.objects.get(pk=zaposlenik_id)
    if request.method == 'POST':
        form = editUserForm(request.POST, instance=zaposlenik)
        if form.is_valid():
            form.save()
            return redirect('korisnik_radilište',korisnik_id=zaposlenik_id)
        else:
            return render(request,'ažuriraj_korisnika.html',{'form':form,'zaposlenik':zaposlenik})
    else:
        form = editUserForm(instance=zaposlenik)
        return render(request,'ažuriraj_korisnika.html',{'form':form,'zaposlenik':zaposlenik})


@login_required
def ažuriraj_pacijenta(request,pacijent_id):
    pacijent=RegistarPacijenata.objects.get(pk=pacijent_id)
    print(pacijent)
    if request.method == 'POST':
        form = AddPacijentForm(request.POST, instance=pacijent)
        if form.is_valid():
            form.save()
            return redirect('profil_pacijent',pacijent_id=pacijent_id)
        else:
            return render(request,'ažuriraj_pacijenta.html',{'form':form,'pacijent':pacijent})
    else:
        form = AddPacijentForm(instance=pacijent)
        print(form)
        return render(request,'ažuriraj_pacijenta.html',{'form':form,'pacijent':pacijent})
    

@login_required
def change_password_zaposlenik(request,zaposlenik_id):
    id=Korisnik.objects.get(pk=zaposlenik_id)
    if request.method == 'POST':
        form = SetPasswordForm(data=request.POST, user=id)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('korisnik_radilište', korisnik_id=zaposlenik_id)
        else:
            return HttpResponse("Something went wrong!")
    else:
        form = SetPasswordForm(user=id)
        args = {'form': form}
        return render(request, 'password.html', args)


def search_pacijent(request):
	if request.method == "POST":
		searched = request.POST['searched']
		pacijent = RegistarPacijenata.objects.filter(Q(ime__contains=searched) | Q(prezime__contains=searched) | Q(MBO__contains=searched))
	
		return render(request, 'search_pacijent.html', {'searched':searched,'pacijent':pacijent})
	else:
		return render(request, 'search_pacijent.html', {})

def search_zaposlenik(request):
	if request.method == "POST":
		searched = request.POST['searched']
		korisnik = Korisnik.objects.filter(Q(username__contains=searched) | Q(first_name__contains=searched) | Q(last_name__contains=searched) | Q(role__contains=searched))
	
		return render(request, 'search_korisnik.html', {'searched':searched,'korisnik':korisnik})
	else:
		return render(request, 'search_korisnik.html', {})

def search_radilište(request):
	if request.method == "POST":
		searched = request.POST['searched']
		radilište = Radilišta.objects.filter(Q(klinika__contains=searched) | Q(naziv__contains=searched))
	
		return render(request, 'search_radilišta.html', {'searched':searched,'radilište':radilište})
	else:
		return render(request, 'search_radilišta.html', {})

def search_utrošak(request):
	if request.method == "POST":
		searched = request.POST['searched']
		utrošak = ŠifrarnikUtrošak.objects.filter(Q(šifra__contains=searched) | Q(naziv__contains=searched))
	
		return render(request, 'search_utrošak.html', {'searched':searched,'utrošak':utrošak})
	else:
		return render(request, 'search_utrošak.html', {})



        
def nalaz_pdf(request,nalaz_id):  
   pass
	
            