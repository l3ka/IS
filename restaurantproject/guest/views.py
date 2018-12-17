from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import logging
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

def home(request):
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

def menu(request):
    context = {
        'dishes': dishes,
        'recommended_dishes': recommended_dishes,
        'recommended_drinks': recommended_drinks,
    }
    return render(request, 'guest/menu.html', context)

def order(request):
    from json import loads
    if request.method == 'POST':
        order_data_json = request.body
        try:
            order_data = loads(order_data_json)
            return JsonResponse({'success': False, 'order': {'id': 'EXAMPLE'}})
            # TODO: Save order
        except (ValueError,TypeError) as e:
            logging.error(e)
            
    return JsonResponse({'success': False, 'error': 'An unknown error occurred.'})

def order_status(request, order_id):
    from json import loads
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Method not allowed.'})
    if not order_id:    
        return JsonResponse({'success': False, 'error': 'Invalid order id.'})
    
    try:
        # TODO: Get order status and return
        pass
        return JsonResponse({'success': True, 'order': {'status' : 'PENDING'}})
    except (ValueError,TypeError) as e:
        logging.error(e)
            
    