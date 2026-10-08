from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Crea los grupos y usuarios de demostración'

    def handle(self, *args, **kwargs):

        operario, _ = Group.objects.get_or_create(
            name='Operario'
        )

        supervisor, _ = Group.objects.get_or_create(
            name='Supervisor'
        )

        jefe, _ = Group.objects.get_or_create(
            name='Jefe'
        )

        usuarios = [
            ('operario_demo', 'operario123', operario),
            ('supervisor_demo', 'supervisor123', supervisor),
            ('jefe_demo', 'jefe123', jefe),
        ]

        for username, password, grupo in usuarios:

            usuario, creado = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': grupo.name,
                }
            )

            if creado:
                usuario.set_password(password)
                usuario.save()

            usuario.groups.clear()
            usuario.groups.add(grupo)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuario configurado: {username} '
                    f'-> {grupo.name}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Grupos y usuarios creados correctamente.'
            )
        )