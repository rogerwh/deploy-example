# Deploy Project

### Comandos para crear el entorno:

Estos comandos se ejecutan en la ruta del proyecto donde se encuentra el archivo `Pipfile`. Todo esto tomando en cuenta que ya se tiene instalado pipenv localmente.

```bash
pipenv shell
pienv install
```

Esto habra instalado django correctamente.

### Comandos para crear el proyecto:

Crear el proyecto por nombre "deploy"

```bash
django-admin startproject deploy
```

Renombramos la carpeta principal por "deployment"

```bash
mv deploy deployment
```

Creamos la carpeta donde se encontraran las aplicaciones

```bash
mkdir -p deploy/apps/
```

Creamos la aplicacion denominada "users"

```bash
django-admin startapp users
```

De esta forma ya podemos correr el proyecto

```bash
./manage.py runserver
```

Tambien puede usarse el siguiente repositorio para crear la estructura del proyecto (como este caso): https://github.com/desarrollowh/django_base

### Correr el proyecto con Supervisor

#### Configurar Nginx

Creamos el archivo de configuración de nginx

```bash
sudo nano /etc/nginx/sites-available/deploy
```

El contenido es el siguiente:

```bash
upstream nDeploy{
    server 127.0.0.1:8809;
}


server {
    # Escuchar en el puerto 80
    listen 80;

    # Para solicitudes a estos dominios
    server_name deploy.io;

    # Buscar en este directorio los archivos a servir
    location /static/ {
        alias /home/roger/Documentos/github/practices/deployment/deployment/static;
        include h5bp/location/expires.conf;
    }

    # Archivos subidos por los usuarios
    location /media/ {
        alias /home/roger/Documentos/github/practices/deployment/deployment/media;
        include h5bp/location/expires.conf;
    }

    # Guardar los logs en los siguientes archivos
    access_log /home/roger/Documentos/github/practices/deployment/deployment/.logs/deploy.log; 
    error_log /home/roger/Documentos/github/practices/deployment/deployment/.logs/deploy.log;

    location / {
	proxy_pass http://nDeploy;
        proxy_redirect  off;

        client_max_body_size    15M;
        client_body_buffer_size 128k;

        proxy_read_timeout  600s;
        proxy_set_header    Host $host;
        proxy_set_header    X-Real-IP $remote_addr;
        proxy_set_header    X-Forwarded-For
        $proxy_add_x_forwarded_for;
    }


    # Codificacion
    charset utf-8;

    # Configuracion Basica
    include h5bp/basic.conf;
}
```

Generamos el link simbolico:

```bash
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/deploy
```

Reiniciamos nginx:

```bash
sudo systemctl restart nginx
```

#### Configurar Supervisor

Nos posicionamos en la ruta de supervisor

```bash
cd /etc/supervisor/conf.d
```

Creamos el siguiente archivo:

```bash
sudo nano deploy.conf
```

Pegamos el siguiente contenido:

```bash
; ==================================
;  deploy project
; ==================================

; the name of your supervisord program
[program:deploy]

; The directory to your Django project
;Directorio del proyecto Django
directory = /path/to/project/

; Set full path to uwsgi file on project using gunicorn path
;Direccion del archivo gunicor que esta en la carpeta del entorno virtual y archivo wsgi en tu proyecto django, conexion a una IP y puerto
command = /path/to/env/deployment-ecirYjpA/bin/gunicorn deploy.core.wsgi:application --bind 127.0.0.1:8809 -w 8 -t 600

; If supervisord is run as the root user, switch users to this UNIX user account
; before doing any processing.
user = ahkin

; Supervisor will start as many instances of this program as named by numprocs
numprocs = 1

; Put process stdout output in this file
; Direccion del log del worker
stdout_logfile = /path/to/project/.logs/supervisor/depĺoy.log

; Put process stderr output in this file
; Direccion del log de errores del worker
stderr_logfile = /path/to/project/deployment/.logs/supervisor/depĺoy.log

; If true, this program will start automatically when supervisord is started
autostart = true

; May be one of false, unexpected, or true. If false, the process will never
; be autorestarted. If unexpected, the process will be restart when the program
; exits with an exit code that is not one of the exit codes associated with this
; process’ configuration (see exitcodes). If true, the process will be
; unconditionally restarted when it exits, without regard to its exit code.
autorestart=true

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true


; ==================================
;  Worker Deploy
; ==================================

; the name of your supervisord program
[program:cDeployWorker]

; Set full path to celery program if using virtualenv
command=/path/to/env/deployment-ecirYjpA/bin/celery -A deploy.core worker --loglevel=INFO

; The directory to your Django project
directory=/path/to/project/

; If supervisord is run as the root user, switch users to this UNIX user account
; before doing any processing.
user=root

; Supervisor will start as many instances of this program as named by numprocs
numprocs=1

; Put process stdout output in this file
stdout_logfile=/path/to/project/.logs/celery/deploy.log

; Put process stderr output in this file
stderr_logfile=/path/to/project/.logs/celery/deploy.log

; If true, this program will start automatically when supervisord is started
autostart=true

; May be one of false, unexpected, or true. If false, the process will never
; be autorestarted. If unexpected, the process will be restart when the program
; exits with an exit code that is not one of the exit codes associated with this
; process’ configuration (see exitcodes). If true, the process will be
; unconditionally restarted when it exits, without regard to its exit code.
autorestart=true

; The total number of seconds which the program needs to stay running after
; a startup to consider the start successful.
startsecs=10

; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true

; if your broker is supervised, set its priority higher
; so it starts first
priority=998

```

Ejecutamos lo siguiente:

```bash
sudo supervisorctl reread
sudo supervisorctl update
```
