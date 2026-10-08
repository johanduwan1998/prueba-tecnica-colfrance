def es_operario(user):
    return user.groups.filter(name='Operario').exists()


def es_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()


def es_jefe(user):
    return user.groups.filter(name='Jefe').exists()