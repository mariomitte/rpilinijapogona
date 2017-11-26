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

def upravljanje_create(request):
    # POST metoda
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Dozvoljeno sa privilegiranim racunom')

    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')
    else:
        form = UpravljanjeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            #print(form.cleaned_data.get('title'))
            instance.user = request.user
            instance.save()
            # message success
            messages.success(request, 'Uspjesno kreirano')
            return HttpResponseRedirect(instance.get_absolute_url())

        context = {
            'form':form,
        }
        return render(request, 'pogon1/upravljanje_form.html', context)
    return render(request, 'pogon1/upravljanje_form.html')

def upravljanje_detail(request, id=None): # retrieve
    #instance = Post.objects.get(id=1)
    instance = get_object_or_404(Upravljanje, id=id)
    context = {
        'title':instance.title,
        'instance':instance,
    }
    return render(request, 'pogon1/upravljanje_detail.html', context)

def upravljanje_list(request): # list items
    if not request.user.is_staff or not request.user.is_superuser:
        messages.error(request, 'Dozvoljeno sa privilegiranim racunom')

    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')

    else:
        queryset = Upravljanje.objects.filter(korisnik=request.user)
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
    return render(request, 'pogon1/upravljanje_list.html')

def upravljanje_update(request, id=None): # retrieve
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Upravljanje, id=id)
    form = UpravljanjeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, 'Uspjesno spremljeno')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title':instance.title,
        'instance':instance,
        'form':form,
    }
    return render(request, 'pogon1/upravljanje_form.html', context)


def upravljanje_delete(request,id=None): # delete
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Upravljanje, id=id)
    instance.delete()
    messages.success(request, 'Uspjesno obrisano')
    return redirect('pogon1:list')

def pogon(request):
    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')
        return render(request, 'pogon1/dokumentacija.html')
    else:
        korisnika_aktivno = User.objects.count()
        queryset = Upravljanje.objects.filter(korisnik=request.user)
        if request.method == 'POST':
            model = request.POST.get('dropdown1')
            Upravljanje.objects.filter(kod='pogon1').update(model=model)
            print(model)
            messages.success(request, 'Odabrano: ' + model)
        else:
            if 'cmd' in request.GET and request.GET['cmd']:
                cmd = request.GET['cmd']

                if cmd == 'record':
                    camera.record()

                if cmd == 'stop-record':
                    camera.stop()

                if cmd == 'take-photo':
                    camera.photo()

                #Upravljanje saRPi3 GPIO pinovima
                motor_control(cmd)

                if (cmd == 'brze') or (cmd =='sporije'):
                    speed_control(cmd)

                # Kreiranje API priključka za pogon1
                Upravljanje.objects.filter(kod='pogon1').update(extra=cmd)


        # if 'cmd' in request.GET and request.GET['cmd']:
        #     cmd = request.GET['cmd']
        #
        #     if (cmd == 'brze') or (cmd =='sporije'):
        #         speed_control(cmd)
        #
        #     motor_control(cmd)

        context = {
            'korisnika_aktivno': korisnika_aktivno,
            'object_list':queryset,
        }

        return render(request, 'pogon1/pogon.html', context)

def dokumentacija(request):
    if not request.user.is_authenticated():
        messages.error(request, 'Potrebno se prijaviti')
    return render(request, 'pogon1/dokumentacija.html')


def upravljanje_prijava(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                obj = Upravljanje.objects.filter(korisnik=request.user)
                messages.success(request, 'Uspjesno prijavljen')
                return render(request, 'pogon1/upravljanje_prijava.html', {'ispitivanje': obj})
            else:
                messages.error(request, 'Tvoj račun je blokiran od strane administratora')
                return render(request, 'pogon1/upravljanje_prijava.html')
        else:
            messages.error(request, 'Neispravni korisnički podaci')
            return render(request, 'pogon1/upravljanje_prijava.html')
    return render(request, 'pogon1/upravljanje_prijava.html')

def upravljanje_odjava(request):
    form = UpravljanjeForm(request.POST or None)
    logout(request)
    messages.success(request, 'Uspjesno odjavljen')
    context = {
        'form': form,
    }
    return render(request, 'pogon1/dokumentacija.html', context)
