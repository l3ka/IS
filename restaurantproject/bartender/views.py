from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime

dishes_first = [
    {
        'img_url': 'img/d1.jpg',
        'name': 'Sendvič sa sirom i voćem',
        'description': 'Sendvič sa bogatim mediteranskim sirom i probranim voćem sa juga Grčke.',
        'price': 8,
        'quantity': 5,
        'note': 'Bez limuna'
    },
    {
        'img_url': 'img/d2.jpg',
        'name': 'Goveđi kotleti sa lukom',
        'description': 'Samo najbolje goveđe meso i svježi probrani luk sa lokalne pijace daju ovom jelu čar i prepoznatljiv okus o kojem ćete pričati prijateljima i porodici.',
        'price': 8,
        'quantity': 1,
        'note': 'Bez luka'
    },
    {
        'img_url': 'img/d3.jpg',
        'name': 'Odrezak u sosu sa povrćem',
        'description': 'Najkvalitetnija junetina od domaćih uzgajača, svježe probrano povrće sa lokalne pijace, vrhunski kuvari. Savršen recept za dobar provod i pun stomak.',
        'price': 8,
        'quantity': 1,
        'note': ''
    }
]

dishes_second = [
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Dupli čizburger',
        'description': 'Ako ste voljeli običan ili onaj dupli, sigurni smo da ćete uživati u ovoj senzaciji. Dupli čizburger ima dva komada 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i dva parčeta američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8,
        'quantity': 2,
        'note': 'Ekstra krastavaca'
    }, 
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Čizburger',
        'description': 'Čizburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i parčetom američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8,
        'quantity': 1,
        'note': ''
    },
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Hamburger',
        'description': 'Hamburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom i senfom. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8,
        'quantity': 1,
        'note': 'Bez kečapa'
    }
]

dishes_third = [
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Dupli čizburger',
        'description': 'Ako ste voljeli običan ili onaj dupli, sigurni smo da ćete uživati u ovoj senzaciji. Dupli čizburger ima dva komada 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i dva parčeta američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8,
        'quantity': 2,
        'note': 'Ekstra krastavaca'
    }, 
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Čizburger',
        'description': 'Čizburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i parčetom američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8,
        'quantity': 1,
        'note': ''
    }
]

orders = [
    {
        'table_number': '3',
        'time_ordered': datetime.datetime.now().strftime('%b.%d.%G - %H:%M:%S'),
        'details': dishes_first,
        'price_together': 56, 
        'id': 1
    },
    {
        'table_number': '11',
        'time_ordered': datetime.datetime.now().strftime('%b.%d.%G - %H:%M:%S'),
        'details': dishes_second,
        'price_together': 32, 
        'id': 2
    },
    {
        'table_number': '2',
        'time_ordered': datetime.datetime.now().strftime('%b.%d.%G - %H:%M:%S'),
        'details': dishes_third,
        'price_together': 24, 
        'id': 3
    },
    {
        'table_number': '5',
        'time_ordered': datetime.datetime.now().strftime('%b.%d.%G - %H:%M:%S'),
        'details': dishes_first,
        'price_together': 56, 
        'id': 4
    },
    {
        'table_number': '12',
        'time_ordered': datetime.datetime.now().strftime('%b.%d.%G - %H:%M:%S'),
        'details': dishes_second,
        'price_together': 32, 
        'id': 5
    },
    {
        'table_number': '4',
        'time_ordered': datetime.datetime.now().strftime('%b.%d.%G - %H:%M:%S'),
        'details': dishes_third,
        'price_together': 24, 
        'id': 6
    }
]

base_props = {
    'restaurant': 'Restoran X'
}

@login_required(login_url='/bartender/login/')
def orders_screen(request):
    if is_member(request.user, 'Konobar'):
        return HttpResponseRedirect(reverse('guest-menu'))
    context = {
        'orders': orders,
    }
    return render(request, 'bartender/orders.html', context)


def login(request):
    return render(request, 'bartender/login.html')

def is_member(user, group):
    return user.groups.filter(name = group).exists()