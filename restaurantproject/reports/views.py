from django.shortcuts import render
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