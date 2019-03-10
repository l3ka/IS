from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from dateutil import parser
from base.models import MeniStavka, Sastojak, SastojakMeniStavka, Narudzba, NarudzbaStavka, NarudzbaStavkaOdabraneOpcije
from base.common.orders import ORDER_STATUSES
from decimal import Decimal

def get_orders(time_ordered=None):
    orders = []
    all_orders = []
    if time_ordered:
        all_orders = Narudzba.objects.filter(vrijemeKreiranja__gt=time_ordered).all().exclude(
            status__in=[ORDER_STATUSES['CANCELLED']['ID'], ORDER_STATUSES['COMPLETED']['ID']])
    else:
        all_orders = Narudzba.objects.all().exclude(
            status__in=[ORDER_STATUSES['CANCELLED']['ID'], ORDER_STATUSES['COMPLETED']['ID']])

    for o in all_orders:
        items = list(o.narudzbastavka_set.all())
        items_mapped = []
        price = Decimal(0)
        for i in items:
            # total_item_price je sad redudantno
            # TODO: Za cijenu bez opcija se na front-endu postavlja cijena sa opcijama.
            total_item_price = i.cijenaBezOpcija # @Nedeljko: iz nekog razloga mi smo kao cijenuBezOpcija slali ukupnu cijenu lol
            price += total_item_price * i.kolicina
            prilozi = list(NarudzbaStavkaOdabraneOpcije.objects.filter(narudzbaStavka=i.id))
            items_mapped.append({
                'img_url': i.meniStavka.fotografija,
                'name': i.meniStavka.naziv,
                'description': i.meniStavka.opis,
                'price': total_item_price,
                'quantity': i.kolicina,
                'note': i.napomena,
                'additions': '\n'.join([ad.naziv for ad in prilozi])
            })

        orders.append({
            'table_number': o.stol,
            'time_ordered': o.vrijemeKreiranja,
            'details': items_mapped,
            'price_together': price,
            'id': o.id,
            'status':  o.status,
            'status_text':  ORDER_STATUSES[o.status]['TEXT']
        })
    return orders

@login_required(login_url='/bartender/login/')
def orders_screen(request):
    if not is_member(request.user, 'Šankeri'):
        return HttpResponseRedirect(reverse('guest-menu'))
    orders = get_orders()
    context = {
        'orders': orders,
    }
    return render(request, 'bartender/orders.html', context)

@login_required(login_url='/bartender/login/')
def orders(request):
    if not is_member(request.user, 'Šankeri'):
        return HttpResponseRedirect(reverse('guest-menu'))
    
    try:
        t = int(request.GET['t'])/1000 + 1 if 't' in request.GET else None
        time_ordered = datetime.datetime.fromtimestamp(t)
    except Exception as ex:
        time_ordered = None

    orders = get_orders(time_ordered)
    context = {
        'orders': orders,
    }
    for order in orders:
        for item in order["details"]:
            item.pop('img_url')
    return JsonResponse({'success': True, 'orders': orders})



def login(request):
    return render(request, 'bartender/login.html')

def is_member(user, group):
    return user.groups.filter(name = group).exists()