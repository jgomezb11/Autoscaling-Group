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

- **MonitorS**:

- **ControllerASG**:

- **MonitorC**:


#### Requisitos No Funcionales:


## Documento Diseño detallado desde el sistema distribuido y software
---
### Análisis


### Diseño


### Arquitectura del despliegue
![Arquitectura de datos](https://raw.githubusercontent.com/juan9572/MOM/main/Diagrams/Diagrama%20de%20arquitectura.png)

### Arquitectura de clases
![Arquitectura de datos](https://raw.githubusercontent.com/juan9572/MOM/main/Diagrams/Diagrama_de_clases.drawio.png)

### Arquitectura de datos
![Arquitectura de datos](https://raw.githubusercontent.com/juan9572/MOM/main/Diagrams/Arquitectura%20de%20datos.png)

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

### Instalacion

Para instalar nuestra solucion en tus servidores es necesario que tengas instaladas todas las dependencias que fueron anteriormente listadas. De esta manera solo seria necesario compilar el archivo.proto que define el paso de mensajes por medio de gRPC para que todo funcione correctamente.

Para esto únicamente hace falta que ejecutes el siguiente comando, el cual instalara todas las dependencias en las versiones requeridas.

```
pip install -r requirements.txt
```


### Ejecución
### Uso
