# Django
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import *
from django.contrib.auth.decorators import *

# Modelos
from .models import Evento, Seleccion, Usuario

def index(request):
    listaEventos = Evento.objects.order_by('-fechaEvento').filter(activo = False)
    eventosActivos = Evento.objects.order_by('-fechaEvento').filter(activo = True)
    context = {'listaEventos': listaEventos, 'eventosActivos': eventosActivos}
    return render(request, 'cenas/index.html', context)

def redirectcenas():
    return redirect(to=reverse('cenas:index'), permanent=True)

def detail(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    dni = request.COOKIES.get('dni', "")
    context = {'evento': evento, 'dnialmacenado': dni}
    return render(request, 'cenas/detail.html', context)

class ResultsView(generic.DetailView):
    model = Evento
    template_name = 'cenas/recuento.html'

def seleccionar(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    try:
        cena_seleccionada = evento.seleccion_set.get(pk=request.POST['cena'])
    except (KeyError, Seleccion.DoesNotExist):
        return render(request, 'cenas/detail.html', {
            'evento': evento,
            'error_message': "No has seleccionado una cena.",
        })
    else:
        if not Usuario.objects.filter(dni=request.POST['dni']).exists():
            return render(request, 'cenas/detail.html', {
                'evento': evento,
                'error_message': "No existe el usuario indicado"
            })

        # Revisa las personas que ya están apuntadas y añadelas a la lisa de apuntados.
        if not Evento.objects.values_list('apuntados', flat=True).get(pk=evento.id):
            usuariosApuntados = []
        else:
            usuariosApuntados = list(Evento.objects.values_list('apuntados', flat=True).get(pk=evento.id))
        
        usuariosApuntadosFlat = []
        apuntado = False
        
        # Comprueba que el usuario esta presente, no guardaremos la nueva lista si existe
        for item in usuariosApuntados:
            if not item == "":
                usuariosApuntadosFlat.append(item)

        for apuntadoActual in usuariosApuntadosFlat:
            if not apuntadoActual:
                break
            if apuntadoActual == request.POST['dni']:
                apuntado = True
                break
            else:
                continue
        
        if apuntado == False:
            usuariosApuntadosFlat.append(request.POST['dni'])

      # Revisa la lista de alégenos si el usuario ha marcado que es alergeno.

        alergeno = request.POST.get('alergeno', False)

        usuariosAlergenosFlat =  []
        
        if alergeno == "True":
            if not Evento.objects.values_list('alergenos', flat=True).get(pk=evento.id):
                usuariosAlergenos = []
            else:
                usuariosAlergenos = list(Evento.objects.values_list('alergenos', flat=True).get(pk=evento.id))
            for item in usuariosAlergenos:
                if not item == "":
                    usuariosAlergenosFlat.append(item)
            if not usuariosAlergenosFlat:
                usuariosAlergenosFlat.append(request.POST['dni'])
        
        if evento.siguienteEvento:
            response = HttpResponseRedirect(reverse('cenas:detail', args=[Evento.objects.values_list('siguienteEvento', flat=True).get(pk=evento.id)]))
        else:
            response = HttpResponseRedirect(reverse('cenas:recuento', args=(evento.id, )))
        
        response.set_cookie('dni', request.POST['dni'], max_age=None, secure=True, httponly=True, samesite='Strict')
        evento.apuntados = usuariosApuntadosFlat
        evento.alergenos = usuariosAlergenosFlat
        evento.save(update_fields=['apuntados', 'alergenos'])

        # Revisa las personas que ya han seleccionado la opcion.
        if not Seleccion.objects.values_list('usuarios', flat=True).get(pk=request.POST['cena']):
            usuariosSeleccion = []
        else:
            usuariosSeleccion = list(Seleccion.objects.values_list('usuarios', flat=True).get(pk=request.POST['cena']))
        
        usuariosSeleccionFlat = []
        seleccionado = False
        
        # Comprueba que el usuario esta presente, no guardaremos la nueva lista si existe
        for item in usuariosSeleccion:
            if not item == "":
                usuariosSeleccionFlat.append(item)

        for usuarioActual in usuariosSeleccionFlat:
            if not usuarioActual:
                break
            if usuarioActual == request.POST['dni']:
                seleccionado = True
                break
            else:
                continue
        
        if seleccionado == False:
            usuariosSeleccionFlat.append(request.POST['dni'])

        cena_seleccionada.recuento += 1
        cena_seleccionada.usuarios = usuariosSeleccionFlat
        cena_seleccionada.save()
        return response

@login_required
def seleccion_evento_obtener(request):
    listaEventos = Evento.objects.order_by('-fechaEvento')
    context = {'listaEventos': listaEventos}
    return render(request, 'accounts/seleccionevento.html', context)

@login_required
def obtener_selecciones(request, evento_id):
    import django_excel as excel

    data = []

    cenas = Seleccion.objects.values_list('cena', flat=True).filter(idEvento=evento_id)
    cenasFlat = []

    for currentCena in cenas:
        if not currentCena == "":
            cenasFlat.append(currentCena)

    for currentCena in cenasFlat:
        usuarios = Seleccion.objects.filter(cena__exact=currentCena).values_list('usuarios', flat=True)
        usuariosFlat = []
        for item in usuarios:
            if item and not item == "":
                for currentUsuario in item:
                    dataUsuario = Usuario.objects.filter(dni__exact=currentUsuario).get()
                    if not dataUsuario:
                        continue
                    nombreCompletoUsuario = dataUsuario.nombre + ' ' + dataUsuario.apellidos
                    usuariosFlat.append(nombreCompletoUsuario)
        data += [[currentCena], usuariosFlat]

    return excel.make_response_from_array(data, 'xlsx', file_name='ListadoSelecciones-' + str(evento_id))
