# Posti (Django) 

Es una aplicación web en Django que permite almacenar pequeñas notas de manera anónima o con un usuario con un editor WYSIWYG que hace la edición más cómoda.
Las notas anónimas se almacenan y no se pueden editar. Las notas con un usuario registrado pueden ser editadas por el propio usuario.
Todas las notas son de acceso público. Las notas ajenas se pueden reportar si es que tienen algún contenido inapropiado. 

## Requerimientos

Están listados en [requirements.txt](requirements.txt) (aparte de Selenium y Firefox con Geckodriver para los tests funcionales, si se quiere pero no es necesario)
  
La aplicación viene con una configuración para usarla con PostgreSQL pero si quieren probarla sólo con sqlite hay que cambiar [settings.py](untitled2/settings.py) para que quede por defecto.

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

También se pueden eliminar las referencias a **whitenoise** en [settings.py](untitled2/settings.py) que son necesarias sólo en un ambiente de producción (cuando no se usa manage.py runserver).

Una vez que esté hecho se puede hacer lo siguiente:

    $ python manage.py test posti.tests.unit
    $ python manage.py collectstatic
    $ python manage.py test posti.tests.selenium (si se desea y Firefox con Geckodriver está configurado)

Si todo está bien:

    $ python manage.py runserver
     
O (en Linux)

    $ gunicorn untitled2.wsgi --log-file - 

(en Windows gunicorn no funciona, se usa waitress).

## Mejoras

Esta aplicación la creé como un modelo sencillo que sirviera de ejemplo para hacer aplicaciones más grandes. De todas maneras se podrían hacer algunas mejoras.

- Crear postis privados (o que los postis de usuarios sean privados per se)
- Habilitar postis de código (a lo pastebin) 
- Mostrar el historial de cada posti
- Cambiar la url SmallUUID por Base62 o algo similar (a lo imgur) para que la URL sea más corta
- Modo blog?

Los reportes por defecto van a la memoria del sistema, pero si se dispone de un servidor SMTP se puede habilitar el envío de esos correos. ([Ver SIBTC]((https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html)) 
Una variación de los reportes podría ser crear un nuevo modelo y almacenar allí todos los reportes. 



## Demo 

Probé la aplicación en heroku y me funcionó con una configuración estándar de acuerdo a la documentación que existe. 
La funcionalidad de subir fotos al editor no funciona porque para eso necesito tener un CDN porque Heroku no almacena las imágenes y de todas maneras los dynos se resetean. 

[DEMO](https://demo-posti.herokuapp.com/)