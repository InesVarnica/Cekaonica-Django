from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Korisnik, Radilišta, RegistarPacijenata, Uputnice, ŠifrarnikUtrošak


# Register your models here.


@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('role',)}),
    )

admin.site.register(Radilišta)
admin.site.register(RegistarPacijenata)
admin.site.register(Uputnice)
admin.site.register(ŠifrarnikUtrošak)