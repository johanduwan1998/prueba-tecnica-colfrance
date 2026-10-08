\# Prueba Técnica Django - Alimentos Colfrance



Aplicación web desarrollada con Python y Django para el registro y gestión de alertas de máquinas y paradas de producción.



\## 1. Tecnologías utilizadas



\- Python 3.13

\- Django

\- SQLite

\- HTML

\- CSS

\- Django Authentication

\- Django Groups para manejo de roles

\- Git y GitHub



\## 2. Funcionalidades



La aplicación permite registrar alertas de máquinas y gestionar paradas de producción de acuerdo con el rol del usuario.



\### Operario



\- Iniciar sesión.

\- Registrar alertas.

\- Consultar únicamente las alertas que él mismo registró.

\- No puede editar alertas.

\- No puede registrar paradas.

\- No puede cancelar paradas.



\### Supervisor



\- Iniciar sesión.

\- Consultar todas las alertas.

\- Editar alertas.

\- Registrar paradas.

\- Consultar las paradas registradas.

\- No puede cancelar paradas.



\### Jefe



\- Iniciar sesión.

\- Consultar todas las alertas.

\- Consultar las paradas.

\- Cancelar una parada.

\- Registrar el usuario, fecha y motivo de la cancelación.

\- No puede editar alertas.

\- No puede registrar paradas.



\## 3. Modelo de datos



\### Alerta



\- Máquina

\- Descripción

\- Usuario que registra

\- Fecha de registro



\### Parada



\- Máquina

\- Fecha y hora de inicio

\- Fecha y hora de finalización

\- Motivo

\- Usuario que registra

\- Duración en minutos

\- Estado de cancelación

\- Usuario que cancela

\- Fecha de cancelación

\- Motivo de cancelación



La información de las cancelaciones no elimina ni modifica el registro original de la parada.



\## 4. Usuarios de demostración



| Usuario | Contraseña | Rol |

|---|---|---|

| operario\_demo | operario123 | Operario |

| supervisor\_demo | supervisor123 | Supervisor |

| jefe\_demo | jefe123 | Jefe |



También se utilizó `operario\_demo\_2` para comprobar que un operario no puede visualizar las alertas registradas por otro operario.



\## 5. Instalación y ejecución



Crear y activar un entorno virtual:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1













Instalar las dependencias:

pip install -r requirements.txt

Ejecutar las migraciones:

python manage.py migrate

Crear los usuarios y grupos de demostración:

python manage.py crear_usuarios

Iniciar el servidor:

python manage.py runserver

Abrir en el navegador:

http://127.0.0.1:8000/
6. Validaciones realizadas
Descripción o motivo vacío

Las alertas no permiten guardar una descripción vacía.

Las paradas no permiten guardar un motivo vacío.

La validación se realiza tanto en los formularios como en los modelos.

Fechas de parada

No se permite registrar una parada cuya fecha de finalización sea menor o igual a la fecha de inicio.

También se contempla correctamente el cambio de día. Por ejemplo:

23:50 → 00:20

corresponde a una duración de:

30 minutos
Permisos

Los permisos se validan en el backend según el grupo del usuario.

Un usuario no autorizado que intente enviar directamente una petición POST para modificar o cancelar información recibe una respuesta de acceso prohibido.

Alertas por operario

Los operarios solamente reciben las alertas asociadas a su propio usuario.

Se utilizó un segundo usuario de prueba (operario_demo_2) para comprobar esta restricción.

Cancelación de paradas

La cancelación no elimina la parada.

Se almacenan:

Usuario que realizó la cancelación.
Fecha y hora.
Motivo de cancelación.

Una parada que ya fue cancelada no puede volver a cancelarse, conservando la primera información registrada.

7. Persistencia

La información se almacena en SQLite mediante el ORM de Django.

Las migraciones se encuentran dentro de:

registro/migrations/

La base de datos SQLite local no se incluye en el repositorio.

8. Casos de resolución de problemas
Caso 1 - Las paradas de producción dejan de registrarse

Primero verificaría el estado de la aplicación y el último error registrado, evitando realizar cambios que puedan agravar el problema. Informaría al responsable de producción sobre el impacto y solicitaría apoyo técnico si no puedo resolverlo con seguridad.

Caso 2 - El jefe necesita un reporte urgente y otro usuario no puede iniciar sesión

Priorizaría según el impacto operativo, informando al jefe sobre el tiempo estimado del reporte y atendiendo o delegando el problema de inicio de sesión. Mantendría comunicación clara sobre los tiempos para evitar afectar ambas necesidades.

Caso 3 - Un cambio propio genera errores

Detendría nuevos cambios, revisaría el error y evaluaría realizar rollback si la modificación está afectando la operación. Informaría al responsable, verificaría la corrección y solamente después continuaría con nuevos cambios.

9. Uso de inteligencia artificial

Se utilizó ChatGPT como herramienta de apoyo durante el desarrollo para estructurar parte de la solución Django, revisar validaciones, permisos, organización del código y documentación.

El código fue revisado y probado localmente durante el desarrollo.

10. Integración en un monolito Django existente

Se reutilizaría el modelo de usuarios existente de Django y sus grupos/permisos para evitar duplicar autenticación.

La aplicación registro podría incorporarse como una app interna del monolito, reutilizando sus modelos, templates y servicios existentes.

Las rutas y permisos se integrarían con la estructura actual del proyecto manteniendo la separación de responsabilidades.

11. Pendientes
No se realizó despliegue en producción porque no fue solicitado.
No se implementaron pruebas automatizadas debido al tiempo disponible y a que no fueron requeridas.
No se implementó OEE ni funcionalidades adicionales fuera del alcance solicitado.
12. Tiempo de desarrollo

El primer commit del proyecto fue realizado el:

2026-10-08 11:54:28 -0500

El commit final de esta versión fue realizado el:

2026-10-08 13:09:55 -0500

Tiempo transcurrido entre ambos commits:

1 hora, 15 minutos y 27 segundos

Primer commit:

83cd1cf

Commit final:

a5d7985
13. Commits principales
Primer commit
83cd1cf - chore: crear proyecto base Django
Commit final
a5d7985 - feat: completar prueba tecnica de alertas y paradas
14. Comprobaciones finales
Django inicia correctamente.
Migraciones ejecutadas correctamente.
Usuarios y grupos creados correctamente.
Login y logout funcionando.
Alertas funcionando según rol.
Registro de paradas funcionando.
Cálculo de duración en minutos funcionando.
Cancelación de paradas conservando la información histórica.
Protección CSRF implementada.
Restricciones de permisos implementadas en backend.
Base de datos local excluida del repositorio.
Dependencias registradas en requirements.txt.