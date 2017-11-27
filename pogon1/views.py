# Function-Based-Views

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UpravljanjeForm
from .models import Upravljanje, camera
from .upravljanje import *

# Kreiranje novog objekta u pogonu
def upravljanje_create(request):
    """Pogled za kreiranje novog objekta."""

    # POST metoda
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Dozvoljeno sa privilegiranim racunom')

    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')

    else:
        form = UpravljanjeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # message success
            messages.success(request, 'Uspjesno kreirano')
            return HttpResponseRedirect(instance.get_absolute_url())

        context = {
            'form':form,
        }
        return render(request, 'pogon1/upravljanje_form.html', context)

    # Ako korisnik nije prijavljen, ne vraća sadržaj pogleda
    return render(request, 'pogon1/upravljanje_form.html')

def upravljanje_detail(request, id=None):
    """Pogled za prikaz detalja kreiranog objekta"""

    instance = get_object_or_404(Upravljanje, id=id)
    context = {
        'title':instance.title,
        'instance':instance,
    }
    return render(request, 'pogon1/upravljanje_detail.html', context)

def upravljanje_list(request):
    """Pogled za prikaz svih kreiranih objekata."""

    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Dozvoljeno sa privilegiranim racunom')

    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')

    else:
        queryset = Upravljanje.objects.filter(korisnik=request.user)

        # Implementirano pretraživanje objekata prema ključnim riječima:
        #     - prema naslovu objekta ili korisnika koji je kreirao objekt
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
    				Q(title__icontains=query)|
    				Q(content__icontains=query)|
    				Q(korisnik__first_name__icontains=query) |
    				Q(korisnik__last_name__icontains=query)
    				).distinct()
        if request.user.is_authenticated:
            context = {
                'title':'Lista objekata',
                'object_list':queryset,
            }
        else:
            context = {
                'title':'List'
            }
        return render(request, 'pogon1/upravljanje_list.html', context)

    # Ako korisnik nije prijavljen, ne vraća sadržaj pogleda
    return render(request, 'pogon1/upravljanje_list.html')

def upravljanje_update(request, id=None): # retrieve
    """Pogled za izmjenu detalja postojećeg objekta."""

    if not request.user.is_staff or not request.user.is_superuser:
        # Ako korisnik nije prijavljen, vraća stranica nije pronađena
        raise Http404
    instance = get_object_or_404(Upravljanje, id=id)
    form = UpravljanjeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # Statusna poruka
        messages.success(request, 'Uspjesno spremljeno')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title':instance.title,
        'instance':instance,
        'form':form,
    }
    return render(request, 'pogon1/upravljanje_form.html', context)


def upravljanje_delete(request,id=None): # delete
    """Pogled za brisanje kreiranog objekta."""

    if not request.user.is_staff or not request.user.is_superuser:
        # Ako korisnik nije prijavljen, vraća stranica nije pronađena
        raise Http404
    instance = get_object_or_404(Upravljanje, id=id)
    instance.delete()
    messages.success(request, 'Uspjesno obrisano')
    # Kada je objekt obrisan, potrebno se vratiti trajnom pogledu
    # Vraćaj pogledu za Prikaz svih kreiranih objekata
    return redirect('pogon1:list')

def pogon(request):
    """Pogled za upravljanje lijom pogona."""

    # Preusmjeri pogled ukoliko korisnik nije prijavljen
    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')
        return render(request, 'pogon1/dokumentacija.html')

    # Prikaži pogled ukoliko je korisnik prijavljen
    else:
        # Odabir objekta kojim se upravlja
        #    - objekti pogona: lanci, sušara, itd.
        korisnika_aktivno = User.objects.count()
        queryset = Upravljanje.objects.filter(korisnik=request.user)
        if request.method == 'POST':
            model = request.POST.get('dropdown1')
            # Ukoliko postoji aplikacija za pogon2, postaviti kod='pogon2'
            # Ukoliko postoji aplikacija za pogon3, postaviti kod='pogon3'
            Upravljanje.objects.filter(kod='pogon1').update(model=model)
            print(model)
            messages.success(request, 'Odabrano: ' + model)
        else:
            # GET metoda
            # Izvrši naredbe pogona koje traži operater
            if 'cmd' in request.GET and request.GET['cmd']:
                cmd = request.GET['cmd']

                # Kamera
                if cmd == 'record':
                    camera.record()

                # Kamera
                if cmd == 'stop-record':
                    camera.stop()

                # Kamera
                if cmd == 'take-photo':
                    camera.photo()

                # RPi3 GPIO upravljanje: Promjena smjera, pauziraj, zaustavi
                motor_control(cmd)

                # RPi3 GPIO pin upravljanje: Promjena brzine
                if (cmd == 'brze') or (cmd =='sporije'):
                    speed_control(cmd)

                # Obavijesti API priključak
                # Za API usluge s kojima radi linija: Telegram
                # Ostaviti ovako za Twitter ili Facebook - ako treba više usluga
                Upravljanje.objects.filter(kod='pogon1').update(extra=cmd)

        context = {
            'korisnika_aktivno': korisnika_aktivno,
            'object_list':queryset,
        }

        return render(request, 'pogon1/pogon.html', context)

def dokumentacija(request):
    """
        Pogled za prikaz dokumentacije pogona.
        Pogled koji se vraća ukoliko korisnik nije prijavljen.
    """

    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')
    return render(request, 'pogon1/dokumentacija.html')


def upravljanje_prijava(request):
    """Pogled za prijavu korisnika u pogon."""

    # POST metoda
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                obj = Upravljanje.objects.filter(korisnik=request.user)
                # Statusna poruka
                messages.success(request, 'Uspjesno prijavljen')
                return render(request, 'pogon1/upravljanje_prijava.html', {'ispitivanje': obj})
            else:
                # Statusna poruka
                messages.error(request, 'Tvoj račun je blokiran od strane administratora')
                return render(request, 'pogon1/upravljanje_prijava.html')
        else:
            messages.error(request, 'Neispravni korisnički podaci')
            return render(request, 'pogon1/upravljanje_prijava.html')

    # Ako korisnik nije prijavljen, ne vraća sadržaj pogleda
    return render(request, 'pogon1/upravljanje_prijava.html')

def upravljanje_odjava(request):
    form = UpravljanjeForm(request.POST or None)
    logout(request)
    # Statusna poruka
    messages.success(request, 'Uspjesno odjavljen')
    context = {
        'form': form,
    }
    return render(request, 'pogon1/dokumentacija.html', context)
