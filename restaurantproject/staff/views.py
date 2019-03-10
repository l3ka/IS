from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required 
def staff_main_view(request):
    context = {
        'isMenadzer': request.user.groups.filter(name='Menadžeri').exists(),
        'isKonobar': request.user.groups.filter(name='Konobari').exists(),
        'isSanker': request.user.groups.filter(name='Šankeri').exists()
    }

    return render(request, 'staff/staff-main-view.html', context)