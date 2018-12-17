from django.contrib import admin

# Register your models here.
from .models import Konobar
from .models import Menadzer
from .models import Stol
from .models import MeniStavka
from .models import Sastojak
from .models import MeniStavkaKategorija

# TODO: Ne bi trebalo da admin sve ovo radi?

admin.site.register(Konobar)
admin.site.register(Menadzer)
admin.site.register(Stol)
admin.site.register(MeniStavka)
admin.site.register(MeniStavkaKategorija)
admin.site.register(Sastojak)