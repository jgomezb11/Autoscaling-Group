# TET-P2
> Definicion de un autoscaling group usando python y boto3.

## Información de la asignatura
---

 -  **Nombre de la asignatura:** Tópicos especiales en telemática.
-   **Código de la asignatura:**  C2361-ST0263-4528
-   **Departamento:** Departamento de Informática y Sistemas (Universidad EAFIT).
-   **Nombre del profesor:** Juan Carlos Montoya Mendoza.
-  **Correo electrónico del docente:** __[jcmontoy@eafit.edu.co](mailto:jcmontoy@eafit.edu.co)__.

## Datos de los estudiantes
---

-   **Nombre del estudiante:** Juan Pablo Rincon Usma.
-  **Correo electrónico del estudiante:** __[jprinconu@eafit.edu.co](mailto:jprinconu@eafit.edu.co)__.
--
-   **Nombre del estudiante:** Donovan Castrillon Franco.
-  **Correo electrónico del estudiante:** __[dcastrillf@eafit.edu.co](mailto:dcastrillf@eafit.edu.co)__.
--
-   **Nombre del estudiante:** Julian Gomez Benitez.
-  **Correo electrónico del estudiante:** __[jgomezb11@eafit.edu.co](mailto:jgomezb11@eafit.edu.co)__.

## Descripcion
---
En los sistemas donde se busca una alta escabilidad en diferentes sistemas distribuidos, se diseñan e implementan mediante servicios de Alta disponibilidad y Rendimiento. Actualmente, existen diferentes servicios en la nube que permiten diseñar e implementar mecanismos para lograr tener una alta disponibilidad y un buen rendimiento. Algunos de estos mecanismos son: Balanceadores de carga (LB) y Grupos de Autoescalamiento (ASG). Los LB permiten distribuir la carga entre varias unidades de procesamiento y también otras funcionalidades como aislar fallas, mejorar rendimiento, etc. Los ASG permiten mediante diferentes métricas adicionar o eliminar unidades de procesamiento.

La finalidad de este proyecto es diseñar e implementar un servicio de autoescalamiento el cual estará conectado a instancias en AWS.

## Documento de Requerimientos
---
#### Requisitos Funcionales:

- **ControllerASG**: Es un proceso o aplicación que corre en la misma instancia del MonitorS. Tiene
acceso a toda la información recolectada por él el MonitorS por medio de memoria
compartida. Este también deberá ejecutar las siguientes acciones:
  * Se comunica con la API SDK de la nube para acceder y ejecutar el servicio de gestión de instancias EC2
  * Deberá definir minInstances (no menor a dos), maxInstance (máx 5
por el tipo de cuenta aws academy), y una política de creación y otra política de
destrucción de instancias.
  * Deberán definir un mecanismo para almacenamiento en el ControllerASG de toda
esta información de configuración.

- **MonitorC**: Es el proceso que tiene cada instancia el cual estará monitoreando como va la carga de procesador de la instancia a la cual pertenece, además deberá cumplir con lo siguiente:
  * Ping/Pong o Heartbeat para detectar vivacidad de la instancia de la
AppInstance
  * GetMetrics: conjunto de métricas como Carga (medida entre 0 y 100% que
mide la carga de una máquina), para efectos de este proyecto, se simuló y se fue modificando esta métrica. Se espera que esta función de
simulación cambie gradualmente y no bruscamente.
  * Registro y Desregistro del MonitorS

- **MonitorS**: Proceso principal de monitoreo que periódicamente consulta el estado de vivacidad
y carga de las instancias de aplicación (AppInstance) en las cuales corre el proceso MonitorC.


### Arquitectura del despliegue
![Arquitectura de datos](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/Diagrama_Arquitectura.png)

## Documento de detalles/dependencia de implementación, instalación y ejecución
---
### Dependencias

| Nombre del paquete | Versión | Descripción |
| --------- | --------- | --------- |
| Python   | 3.11   | Lenguaje de programacion usado   |
| pymongo   | 4.3.3   | Libreria para establecer conexion con MongoDB   |
| python-dotenv   | 1.0.0   | Libreria para acceder a variables de entorno   |
| dash   | 2.9.3 | Dash es el marco original de código bajo para crear rápidamente aplicaciones de datos en Python. |
| pandas   | 2.0.1 | pandas es una biblioteca para la manipulación y el análisis de datos. |
| boto3   | 1.26.133  | Utiliza el SDK de AWS para Python (Boto3) para crear, configurar y administrar los servicios de AWS |
| grpcio   | 1.53.0   | La librería grpc para Python proporciona una forma de utilizar gRPC en aplicaciones Python   |
| grpcio-tools   | 1.53.0   | La librería grpc para Python proporciona herramientas para usar grpc   |

### Instalacion y Ejecución

Para instalar nuestra solucion en tus servidores es necesario que tengas instaladas todas las dependencias que fueron anteriormente listadas. De esta manera solo seria necesario compilar el archivo.proto que define el paso de mensajes por medio de gRPC para que todo funcione correctamente.

Para esto únicamente hace falta que ejecutes el siguiente comando, el cual instalara todas las dependencias en las versiones requeridas.

```
pip install -r requirements.txt
```

MONITORS:

* Instalar Docker:

- Desinstalar versiones antiguas de Docker usando el siguiente comando:

sudo apt-get remove docker docker-engine docker.io containerd runc

- Configurar el repositorio Ubuntu usando los siguientes comandos:

```
sudo apt-get update
```
```
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg
```

- Añadir la clave GPG oficial de Docker usando el siguiente comando:

```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

- Usar el siguiente comando para configurar el repositorio:

```
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- Actualizar la lista de paquetes usando el siguiente comando:

```
sudo apt-get update
```

- Instalar Docker Engine, containerd y Docker Compose usando el siguiente comando:

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

* Clonar repositorios

```
sudo git clone https://github.com/jgomezb11/TET-P2.git
```

- Hacer build de la imagen y correr los contenedores:

```
cd TET-P2/Docker/Instance
sudo docker compose up -d
```

DATABASE:

* Instalar mongodb:

```
sudo apt update && apt install dirmngr gnupg apt-transport-https ca-certificates software-properties-common
sudo wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
sudo echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt update && sudo apt install -y mongodb-org
sudo wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo apt-get install -y mongodb-org
sudo systemctl enable mongod
sudo systemctl start mongod
```
```
sudo nano /etc/mongod.conf
```
```
bindIp: 0.0.0.0
```
```
sudo systemctl restart mongod
```

### Agregamos el documento a la base de datos de ASG en la colección config:
![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/db-1.png)
![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/db-2.png)
![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/db-3.png)
![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/db-4.png)

```
{
  "_id": {
    "$oid": "64619b3dc46f0c7812d5086f"
  },
  "average_memory": 0,
  "hosts": [],
  "status": [],
  "min_instances": 2,
  "max_instances": 5,
  "scale_up_factor": 2,
  "scale_down_factor": 0.5,
  "cpu_up_threshold": 70,
  "cpu_down_threshold": 20
}
```

ASG:

* Instalar docker:

- Desinstalar versiones antiguas de Docker usando el siguiente comando:

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

- Configurar el repositorio Ubuntu usando los siguientes comandos:

```
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg
```

- Añadir la clave GPG oficial de Docker usando el siguiente comando:

```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

- Usar el siguiente comando para configurar el repositorio:

```
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- Actualizar la lista de paquetes usando el siguiente comando:

```
sudo apt-get update
```

- Instalar Docker Engine, containerd y Docker Compose usando el siguiente comando:

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

* Clonar repositorio:

```
sudo git clone https://github.com/jgomezb11/TET-P2.git
```

* Poner las credenciales, la región en las variables de entorno:

```
sudo nano TET-P2/Docker/Auto\ Scalling\ Group/.env
```

* Crear los contenedores y correrlos

```
cd TET-P2/Docker/Auto\ Scalling\ Group
sudo docker compose up -d
```

### Uso

A la hora de ingresar al sistema lo primero con los que nos encontraremos sera con un panel de configuracion:

![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/plot-1.png)

En donde podremos elegir los parámetros al nuestro interés:

* Min Instances: Es el número mínimo de instancias que queremos que se estén ejecutando simultáneamente
* Max Instances: Es el número máximo de instancias que queremos que se lleguen a estar ejecutando simultáneamente
* CPU Up Threshold: Es el límite superior en el cual si se alcanza se aumenten la cantidad instancias actuales
* CPU Down Threshold: Es el límite inferior en el cual si se alcanza queremos que se reduzcan la cantidad de instancias actuales
* Scale Up Factor: Es el factor con el que queremos que en dado caso que se supere el límite superior definido de CPU, estas aumenten su cantidad. Ej: si se tiene en 2, cada vez que se supere el límite superior estas se duplican
* Scale Down Factor: Es el factor con el que queremos que en dado caso que se supere el límite inferior definido de CPU, estas disminuyan su cantidad. Ej: si se tiene en 0.5, cada vez que se supere el límite inferior estas se reducen a la mitad

Ademas de este panel, a continuacion podremos encontrar diferentes graficas sobre el estado de las instancias:

1. El promedio de uso de CPU de todas las instancias actuales

![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/plot-2.png)

2. Una grafica del cambio de uso de CPU por cada instancia activa.

![](https://raw.githubusercontent.com/jgomezb11/TET-P2/main/static/plot-3.png)

