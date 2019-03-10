from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from . import graphing_util

import pandas as pd

# Create your views here.
def index(request):
    return render(request, 'reports/generator.html')

def report(request):
    if request.method == 'POST':
        narudzbe = pd.read_csv('narudzbe.csv')
        narudzbe['date'] = pd.to_datetime(narudzbe['date'])
        narudzbe['just_date'] = narudzbe['date'].dt.date
        dateFrom = request.POST.get('dateFrom', '')
        dateTo = request.POST.get('dateTo', '')
        narudzbe["date"] = narudzbe["date"].astype("datetime64")

        # ovo je i po satu i min i sek
        mask = (narudzbe['date'] > dateFrom) & (narudzbe['date'] <= dateTo)
        narudzbe = narudzbe.loc[mask] # filtrirano
        narudzbe_gr1 = narudzbe.groupby('date', as_index=False).agg({"cijena" : "sum"})
        cijena_ts = graphing_util.plot_timeseries(narudzbe_gr1, 'Zarada po danu', 'cijena')

        # samo po  danu
        narudzbe_gr2 = narudzbe.groupby('just_date', as_index=False).agg({"cijena" : "sum"})
        narudzbe_gr2['date'] = narudzbe_gr2['just_date']
        cijena_ts_date = graphing_util.plot_timeseries(narudzbe_gr2, 'Zarada po danu', 'cijena')

        # ovi grafici prikazuju koliko ima cega po kategorijama prodatog
        stavke = pd.read_csv('stavke.csv')
        prodaja_po_kategoriji = stavke.groupby(['kategorija']).size()
        bar = graphing_util.plot_bar(prodaja_po_kategoriji, prodaja_po_kategoriji.index.values)
        pie = graphing_util.plot_pie(prodaja_po_kategoriji, prodaja_po_kategoriji.index.values)

        # ovaj grafik prikazuje zaradu po kategoriji za neki vremenski period
        profit = stavke.groupby(['kategorija']).sum()
        category_profit_bar = graphing_util.plot_bar(profit.cijena, profit.index.values)

        return render(request, 'reports/reports.html', {
            'cijena_ts' : cijena_ts,
            'bar' : bar,
            'pie' : pie,
            'profit': category_profit_bar,
            'cijena_ts_date' : cijena_ts_date,
        })
    else:
        return redirect('/') # TODO: Skontati gdje treba redirect @Stefan

def generate_report(request):
    return render(request,
        'bartender/report_generator.html'
        )
    # if is_member(request.user, 'Menadžeri'):

    # else:
    #     return redirect('/') # TODO: Skontati gdje treba redirect @Stefan

def is_member(user, group):
    return user.groups.filter(name = group).exists()

# TODO: @Stefan, po potrebi premjestiti u poseban app za menadzere i samo njima dozvoliti da gledaju        !
def reports_old(request):
    if is_member(request.user, 'Menadžeri') and request.method == 'POST':
        dateFrom = request.POST.get('dateFrom', '')
        dateTo = request.POST.get('dateTo', '')
        # X - naziv kategorije, Y - ukupna prodaja
        counts = []
        labels = []

        from base.models import MeniStavkaKategorija
        kategorije = MeniStavkaKategorija.objects.all()
        for kategorija in kategorije:
            from base.models import NarudzbaStavka
            from django.db.models import Sum
            stavke = NarudzbaStavka.objects.filter(meniStavka__meniStavkaKategorija = kategorija)
            suma = sum(stavka.cijenaSaOpcijama for stavka in stavke)
            if suma != 0:
                labels.append(kategorija.naziv)
                counts.append(suma)

        # counts = [10, 15, 30, 40, 33, 141, 20, 15]
        # labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        pie = graphing_util.plot_pie(counts, labels)
        bar = graphing_util.plot_bar(counts, labels)
        return render(request,
                'bartender/graphs.html',
                {
                    'pie' : pie,
                    'bar' : bar,
                })
    else:
        return redirect('/') # TODO: Skontati gdje treba redirect @Stefan