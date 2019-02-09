from django.contrib import admin

# Register your models here.
from .models import Konobar
from .models import Menadzer
from .models import Stol
from .models import MeniStavka
from .models import Sastojak
from .models import MeniStavkaKategorija
from .models import Opcija
from .models import GrupaOpcija
from .models import MeniStavkaTag
from .models import SastojakMeniStavka
from .models import Narudzba
from .models import NarudzbaStavka

# TODO: Ne bi trebalo da admin sve ovo radi?

admin.site.register(Konobar)
admin.site.register(Menadzer)
admin.site.register(Stol)
admin.site.register(MeniStavka)
admin.site.register(MeniStavkaKategorija)
admin.site.register(Sastojak)
admin.site.register(Opcija)
admin.site.register(GrupaOpcija)
admin.site.register(MeniStavkaTag)
admin.site.register(SastojakMeniStavka)
admin.site.register(Narudzba)
admin.site.register(NarudzbaStavka)