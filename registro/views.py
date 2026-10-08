from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlertaForm, ParadaForm
from .models import Alerta, Parada
from .utils import es_operario, es_supervisor, es_jefe


def login_view(request):

    if request.user.is_authenticated:
        return redirect('inicio')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('inicio')

        error = 'Usuario o contraseña incorrectos.'

    return render(
        request,
        'registro/login.html',
        {'error': error}
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def inicio(request):

    usuario = request.user

    # ---------------------------------
    # CREAR ALERTA
    # ---------------------------------
    alerta_form = AlertaForm()

    if request.method == 'POST' and request.POST.get('accion') == 'crear_alerta':

        if not es_operario(usuario):
            return HttpResponseForbidden(
                'No tienes permiso para registrar alertas.'
            )

        alerta_form = AlertaForm(request.POST)

        if alerta_form.is_valid():
            alerta = alerta_form.save(commit=False)
            alerta.usuario = usuario
            alerta.save()

            return redirect('inicio')

    # ---------------------------------
    # CREAR PARADA
    # ---------------------------------
    parada_form = ParadaForm()

    if request.method == 'POST' and request.POST.get('accion') == 'crear_parada':

        if not es_supervisor(usuario):
            return HttpResponseForbidden(
                'No tienes permiso para registrar paradas.'
            )

        parada_form = ParadaForm(request.POST)

        if parada_form.is_valid():
            parada = parada_form.save(commit=False)
            parada.usuario = usuario
            parada.save()

            return redirect('inicio')

    # ---------------------------------
    # EDITAR ALERTA
    # ---------------------------------
    if request.method == 'POST' and request.POST.get('accion') == 'editar_alerta':

        if not es_supervisor(usuario):
            return HttpResponseForbidden(
                'No tienes permiso para editar alertas.'
            )

        alerta_id = request.POST.get('alerta_id')

        alerta = get_object_or_404(
            Alerta,
            id=alerta_id
        )

        alerta_form = AlertaForm(
            request.POST,
            instance=alerta
        )

        if alerta_form.is_valid():
            alerta_form.save()

            return redirect('inicio')

    # ---------------------------------
    # CANCELAR PARADA
    # ---------------------------------
    if request.method == 'POST' and request.POST.get('accion') == 'cancelar_parada':

        if not es_jefe(usuario):
            return HttpResponseForbidden(
                'No tienes permiso para cancelar paradas.'
            )

        parada_id = request.POST.get('parada_id')

        parada = get_object_or_404(
            Parada,
            id=parada_id
        )

        # Si ya fue cancelada, no se modifica.
        if parada.cancelada:
            return HttpResponseForbidden(
                'Esta parada ya fue cancelada y no puede volver a cancelarse.'
            )

        motivo_cancelacion = request.POST.get(
            'motivo_cancelacion',
            ''
        ).strip()

        if not motivo_cancelacion:
            return HttpResponseForbidden(
                'El motivo de cancelación es obligatorio.'
            )

        parada.cancelada = True
        parada.cancelada_por = usuario
        parada.motivo_cancelacion = motivo_cancelacion

        from django.utils import timezone

        parada.fecha_cancelacion = timezone.now()

        parada.save(
            update_fields=[
                'cancelada',
                'cancelada_por',
                'motivo_cancelacion',
                'fecha_cancelacion'
            ]
        )

        return redirect('inicio')

    # ---------------------------------
    # ALERTAS SEGÚN ROL
    # ---------------------------------

    if es_operario(usuario):
        alertas = Alerta.objects.filter(
            usuario=usuario
        ).select_related('usuario')

    else:
        alertas = Alerta.objects.all().select_related('usuario')

    alertas = alertas.order_by('-fecha')

    # ---------------------------------
    # PARADAS
    # ---------------------------------

    paradas = Parada.objects.all().select_related(
        'usuario',
        'cancelada_por'
    ).order_by('-inicio')

    contexto = {
        'alerta_form': alerta_form,
        'parada_form': parada_form,
        'alertas': alertas,
        'paradas': paradas,
        'es_operario': es_operario(usuario),
        'es_supervisor': es_supervisor(usuario),
        'es_jefe': es_jefe(usuario),
    }

    return render(
        request,
        'registro/inicio.html',
        contexto
    )