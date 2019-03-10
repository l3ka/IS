from django.contrib.auth.decorators import login_required
from base.models import Poziv
from django.shortcuts import render
from django.http import JsonResponse

@login_required
def waiter_view(request):
    return render(request, 'waiter/calls.html')

# TODO: Mechanism to tag calls as 'handled'.
@login_required 
def calls(request):
    from datetime import datetime, timedelta

    # HACK: Apparently this gets the local time zone?
    local_timezone = datetime.utcnow().astimezone().tzinfo

    # Filter calls. Get only those made within the last hour.
    time_threshold = datetime.now() - timedelta(hours=1)
    filtered_calls = Poziv.objects.filter(vrijemeKreiranja__gte=time_threshold)

    # Sort calls from latest to oldest.
    sorted_calls = sorted(filtered_calls, key=lambda e : e.vrijemeKreiranja, reverse=True)
    
    response = []
    for call in sorted_calls:
        response.append({
            'sectionNo': call.brojSekcije,
            'tableNo': call.brojStola,
            'datetime': call.vrijemeKreiranja.astimezone(local_timezone) # Converted from UTC to local TZ.
        })
    
    return JsonResponse({'calls': response})