# Django
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseBase, HttpResponseForbidden, HttpResponseGone, HttpResponseNotAllowed, HttpResponseRedirectBase
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth import *
from django.contrib.auth.decorators import *

def logear(request):

    response = render(request, 'accounts/login.html')

    return response

def autenticar(request):

    if not request.POST:
        return HttpResponseNotAllowed(['POST'])

    if request.COOKIES.get('sessionid'):
        return HttpResponseRedirect(reverse('cenas:accounts-panel'))

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('cenas:accounts-panel'))
    else:
        error = "Usuario y/o contraseña incorrectos"
        context = { "error": error }
        return HttpResponseForbidden(render(request, 'accounts/login.html', context))

@login_required()
def panel(request):
    return HttpResponse(render(request, 'accounts/panel.html'))

@login_required()
def cerrarsesion(request):
    logout(request)
    return HttpResponseRedirect(reverse("cenas:index"))
