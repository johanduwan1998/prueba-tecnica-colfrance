from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Alerta(models.Model):
    maquina = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='alertas'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.descripcion or not self.descripcion.strip():
            raise ValidationError({
                'descripcion': 'La descripción no puede estar vacía.'
            })

    def __str__(self):
        return f'{self.maquina} - {self.fecha:%Y-%m-%d %H:%M}'


class Parada(models.Model):
    maquina = models.CharField(max_length=100)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    motivo = models.TextField()

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='paradas_creadas'
    )

    cancelada = models.BooleanField(default=False)

    cancelada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='paradas_canceladas',
        null=True,
        blank=True
    )

    fecha_cancelacion = models.DateTimeField(
        null=True,
        blank=True
    )

    motivo_cancelacion = models.TextField(
        blank=True
    )

    def clean(self):
        errores = {}

        if not self.motivo or not self.motivo.strip():
            errores['motivo'] = 'El motivo no puede estar vacío.'

        if self.inicio and self.fin and self.fin <= self.inicio:
            errores['fin'] = (
                'La fecha y hora de finalización debe ser posterior '
                'a la fecha y hora de inicio.'
            )

        if errores:
            raise ValidationError(errores)

    @property
    def duracion_minutos(self):
        if not self.inicio or not self.fin:
            return 0

        segundos = (self.fin - self.inicio).total_seconds()
        return int(segundos // 60)

    def __str__(self):
        return f'{self.maquina} - {self.inicio:%Y-%m-%d %H:%M}'