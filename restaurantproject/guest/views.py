from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
import logging
import requests
import os
from base.models import MeniStavka, Sastojak, SastojakMeniStavka, Narudzba, NarudzbaStavka, GrupaOpcija, Opcija, OpcijaSastojak, NarudzbaStavkaOdabraneOpcije
from base.common.orders import ORDER_STATUSES
# Create your views here.

base_props = {
    'restaurant': 'Restoran X'
}

dishes = [
    {
        'img_url': 'img/d1.jpg',
        'name': 'Sendvič sa sirom i voćem',
        'description': 'Sendvič sa bogatim mediteranskim sirom i probranim voćem sa juga Grčke.',
        'price': 8
    },
    {
        'img_url': 'img/d2.jpg',
        'name': 'Goveđi kotleti sa lukom',
        'description': 'Samo najbolje goveđe meso i svježi probrani luk sa lokalne pijace daju ovom jelu čar i prepoznatljiv okus o kojem ćete pričati prijateljima i porodici.',
        'price': 8
    },
    {
        'img_url': 'img/d3.jpg',
        'name': 'Odrezak u sosu sa povrćem',
        'description': 'Najkvalitetnija junetina od domaćih uzgajača, svježe probrano povrće sa lokalne pijace, vrhunski kuvari. Savršen recept za dobar provod i pun stomak.',
        'price': 8
    }
]

recommended_dishes = [
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Dupli čizburger',
        'description': 'Ako ste voljeli običan ili onaj dupli, sigurni smo da ćete uživati u ovoj senzaciji. Dupli čizburger ima dva komada 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i dva parčeta američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8
    },
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Čizburger',
        'description': 'Čizburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i parčetom američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8
    },
    {
        'img_url': 'img/slider1.jpg',
        'name': 'Hamburger',
        'description': 'Hamburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom i senfom. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.',
        'price': 8
    }
]

staff = [
    {
        'name': 'Ethel Davis',
        'job_description': 'Glavni kuvar',
        'profile_pic': 'img/t1.jpg'
    },
    {
        'name': 'Rodney Cooper',
        'job_description': 'Glavni konobar',
        'profile_pic': 'img/t2.jpg'
    },
    {
        'name': 'Dora Walker',
        'job_description': 'Šanker',
        'profile_pic': 'img/t3.jpg'
    },
    {
        'name': 'Lena Keller',
        'job_description': 'Pomoćni kuvar',
        'profile_pic': 'img/t4.jpg'
    }
]

impressions = [
    {
        'title': 'Piletina u susamu',
        'date': '10 Jan 2018',
        'likes': '15',
        'comments': '2',
        'content': 'Najbolja hrana u gradu!!!'
    },
    {
        'title': 'Usluga',
        'date': '14 Jul 2018',
        'likes': '7',
        'comments': '1',
        'content': 'Sve u svemu odličan lokal i ambijent, samo se dugo zna čekati na hranu'
    },
    {
        'title': 'Muzika',
        'date': '22 May 2018',
        'likes': '10',
        'comments': '7',
        'content': 'Odlična muzika, svirke uživo su među najboljim što grad može da ponudi'
    },
    {
        'title': 'Piletina u sosu od kikirikija',
        'date': '13 Apr 2018',
        'likes': '32',
        'comments': '12',
        'content': 'NOVO OMILJENO JELO!!! SVE POHVALE KUVARU!!!'
    }
]

recommended_drinks = [
    {
        'img_url': 'img/drink1.jpg',
        'name': 'Johnnie Walker Blue',
        'description': 'Dok nas nijedna druga boja Johnnie Walker-a ne oduševljava, svaki ima malo elemenata koje nas slučajno oduševe. Ovi dobri elementi udružuju snage kako bi stvorili Johnnie Valker Blue. To je kao Voltron. Johnnie Walker Blue je žvakljiv i gladak sa balansom od karamela, dima i zemljanih tonova, što znači da je Johnnie Valker samo želeo da podeli najbolje što je imao da ponudi. To nije najbolji scotch kojeg smo ikada imali, ali to je "veliki" škotski štok, kojeg čak i ljudi koji ne piju znaju.',
        'price': 8
    },
    {
        'img_url': 'img/drink2.jpg',
        'name': 'Cabernet Sauvignon',
        'description': '2014 Cabernet Sauvignon Mayacamas vinograda je graciozan povratak u obliku iz ikone Napa vinarije. Promene u vlasništvu, građanski sporovi i brige o odlasku iz tradicionalnog, elegantnog stila vinarije postaju daleke uspomene prilikom ukusa ovog moćnog ali fokusiranog vina. Veoma lagan hrastov uticaj dozvoljava da sjajni, sunčano natopljen karakter Mount Veeder-a. Kiselost je sjajna, a vino ima kiselog, sočnog crnog voća. Bilje i crni slatki korijen dodaju nijansu, dok su žvakani tanini uporni u trajnom završetku, koji je bogat kamenim mineralnim notama. Ako su vam prekomerno izduvani Napa Cabs okrenuli daleko od sorte i regije, ova boca obećava da vas vraća unazad. Vintage izuzetno dobro pije, ali je i dalje beba. Ovo vino sazreće sa milosrćnošću i elegancijom i može se ostaviti u podrumu decenijama.',
        'price': 8
    },
    {
        'img_url': 'img/drink3.jpg',
        'name': 'Red Rooster Coffee',
        'description': 'Uravnoteženo, bogato slatko, tarto i ukusno. Fini mošus, osušeni cvet hibiskusa, perik (fermentirani) sušeni duvan, pečurke i šampinjone, aroma kajsije. Slatko-tart-ukusna struktura s pikantnom kiselinom; lagano kremasto, nezasitan okus. Bogato tonirana završna obrada oko marelica i odiše umami note slične gljivicama sa šampinjonima.',
        'price': 8
    }
]
from django.middleware.csrf import get_token
def home(request):
    # TODO: Come up with a better solution.
    # Force-get the CSRF token
    csrf_token = get_token(request)
    context = {
        'base_props': base_props,
        'dishes': dishes,
        'recommended_dishes': recommended_dishes,
        'staff': staff,
        'impressions': impressions,
        'recommended_drinks': recommended_drinks,
        'is_main_page': True
    }
    return render(request, 'guest/home.html', context)


def menu_item_additions(request, menu_item_id):
    additionsGroup = GrupaOpcija.objects.filter(meniStavka=menu_item_id)
    res = []
    for gr in additionsGroup:

        temp_res = {
            'id': gr.id,
            'name': gr.naziv,
            'required': gr.jeObavezno,
            'single': gr.jeIskljucivOdabir,
            'options': []
        }

        optionsInGroup = Opcija.objects.filter(grupaOpcija=gr.id)
        for option in optionsInGroup:
            ingredients = [ingr.sastojak for ingr in OpcijaSastojak.objects.filter(
                opcija=option.id)] if option.imaDodatneSastojke else []
            temp_res['options'].append({
                'id': option.id,
                'name': option.naziv,
                'price': option.cijena,
                'ingredients': ','.join(ingredients)
            })

        res.append(temp_res)

    return JsonResponse({'success': True, 'groups': res})


def menu(request):
    # TODO: Come up with a better solution.
    # Force-get the CSRF token
    csrf_token = get_token(request)
    meniStavke_temp = MeniStavka.objects.all()

    # meniStavka['Dorucak'] = ['dorucak1', 'dorucak2'...]
    meniStavke = {}

    for meniStavka in meniStavke_temp:
        # Dodaj spisak sastojaka na meniStavka da se na osnovu njega moze popuniti lista sastojaka pri prikazu.
        meniStavka.sastojci = ''.join([s.sastojak.naziv + ' ' + str(s.kolicina) + "," for s in meniStavka.sastojakmenistavka_set.all()])
        
        naziv = meniStavka.meniStavkaKategorija.naziv
        if meniStavka.meniStavkaKategorija.naziv in meniStavke:
            meniStavke[naziv].append(meniStavka)
        else:
            meniStavke[naziv] = [meniStavka]

    context = {
        'meniStavke': meniStavke
    }
    return render(request, 'guest/menu.html', context)


def add_order(request):
    from json import loads
    if request.method.strip("{}") == 'POST':
        order_data_json = request.body
        try:
            order_data = loads(order_data_json)
            narudzba = Narudzba()
            
            narudzba.save()
            for arr in order_data.values():
                for rb, dict_elem in enumerate(arr):
                    # jer nam ime ne treba pri inicijalizaciji
                    naziv = dict_elem.pop('name', None)
                    narudzba.pushEndpoint = dict_elem.pop('pushEndpoint')
                    narudzba.save()
                    # TODO: Pozeljno je da se na front-end popravi da JSON bude u skladu sa odgovarajucim modelom, pa ovo ne mora da se radi (jer je dupli posao)
                    dict_elem['cijenaBezOpcija'] = dict_elem.pop('price')
                    dict_elem['napomena'] = dict_elem.pop('note')
                    dict_elem['kolicina'] = dict_elem.pop('amount')
                    dict_elem['redniBroj'] = rb + 1
                    dict_elem['napomena'] = dict_elem['napomena'] if 'napomena' in dict_elem else ' '
                    dict_elem.pop('id', None)
                    optionGroups = dict_elem.pop('options')

                    # morao sam preimenovati da bih ovo mogao uraditi
                    narudzbaStavka = NarudzbaStavka(**dict_elem)
                    narudzbaStavka.narudzba = narudzba
                    narudzbaStavka.meniStavka = MeniStavka.objects.filter(
                        naziv=naziv).first()
                    narudzbaStavka.save()

                    for optG in optionGroups['groups']:
                        for selected in optG['selected']:
                            stavkaOpcija = NarudzbaStavkaOdabraneOpcije()
                            stavkaOpcija.naziv = selected['name']
                            stavkaOpcija.cijena = selected['price']
                            stavkaOpcija.opcija = Opcija.objects.get(
                                id=selected['id'])
                            stavkaOpcija.narudzbaStavka = narudzbaStavka
                            stavkaOpcija.save()

            return JsonResponse({'success': True, 'order': {'id': narudzba.id}})
        except (ValueError, TypeError) as e:
            logging.error(e)
            return JsonResponse({'success': False, 'error': str(e)})


def order(request, order_id):
    from json import loads
    if request.method == "PATCH":
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required.'})

        try:
            order_data = loads(request.body)
        except Exception as ex:
            return JsonResponse({'success': False, 'error': 'Invalid payload.'})

        order = Narudzba.objects.get(id=int(order_id))
        order_status = order_data["status"]
        old_status = order.status
        order.status = order_status
        if order_status == ORDER_STATUSES['PROCESSING']['ID']:
            order.jePrihvacena = True
        elif order_status == ORDER_STATUSES['CANCELLED']['ID']:
            order.razlogOdbijanja = order_data["reason"] if "reason" in order_data else ''
        elif order_status == ORDER_STATUSES['READY']['ID']:
            pass
        else:
            return JsonResponse({'success': False, 'error': 'Invalid order status ID.'})
        order.save()

        if order_status != old_status:
            if order.pushEndpoint:
                res = data = requests.post(order.pushEndpoint, headers={
                'TTL': '60',
                'Authorization': 'key={}'.format(settings.PUSH_SERVER_KEY)
                })
                res_t = res.text
            

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'An unknown error occurred.'})


def order_status(request, order_id):
    from json import loads
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Method not allowed.'})
    if not order_id:
        return JsonResponse({'success': False, 'error': 'Invalid order id.'})

    try:
        # TODO: Get order status and return
        order = Narudzba.objects.get(id=order_id)
        # order_status = 'AWAITING_PROCESSING'
        # if order.jePrihvacena:
        #     order_status = 'PROCESSING'
        # elif order.razlogOdbijanja:
        #     order_status = 'CANCELLED'
        res = {'status': order.status}
        if order.status == 'CANCELLED' and order.razlogOdbijanja:
            res['reason'] = order.razlogOdbijanja
        return JsonResponse({'success': True, 'order': res})
    except (ValueError, TypeError) as e:
        logging.error(e)

def serviceworker(req):
    path = os.path.join(settings.PROJECT_PATH, 'guest/static/js/sw.js')
    try:
        test_file = open(path, 'rb')
    except Exception as ex:
        return HttpResponse(content=None)
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/javascript'
    return response

def appmanifest(req):
    path = os.path.join(settings.PROJECT_PATH, 'guest/static/manifest.json')
    try:
        test_file = open(path, 'rb')
    except Exception as ex:
        return HttpResponse(content=None)
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/json'
    return response

def localforage(req):
    path = os.path.join(settings.PROJECT_PATH, 'guest/static/js/localforage.min.js')
    try:
        test_file = open(path, 'rb')
    except Exception as ex:
        return HttpResponse(content=None)
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/javascript'
    return response