# LTM_Challenge


## Parte 1: Infraestructura e IaC

La infraestructura a desplegar tiene como objetivo desarrollar un sistema en la nube que permite ingestar 
datos desde múltiples fuentes (Aplicaciones, dispositivos IoT, etc), almacenarlos en una base de 
datos optimizada para analítica (BigQuery) y exponerlos a través de una API HTTP. 
Porpongo una arquitectura completamente serverless para maximizar la escalabilidad y reducir 
la complejidad operativa.

### Tecnologías Utilizadas.- 

- **Google Cloud Pub/Sub:** Para la ingesta de datos desde diversas fuentes.
- **Google Cloud Functions:** Para el procesamiento y almacenamiento de los mensajes recibidos desde Pub/Sub.
- **Google BigQuery:** Como base de datos para almacenar y futuro analicis los datos recibidos.
- **Google Cloud Run:** Para el despliegue de la API HTTP que expone los datos almacenados en BigQuery.
- **Identity Aware Proxy (IAP):** Con el uso de IAP nos aseguramos que solo los usuarios auteticados puedan 
acceder a la API. Ademas que nos evitamos manejar la autenticacion dento de la API.
- **Cloud Build:** Como herramienta de CI/CD se utilizo Cloud Build que es una solucion nativa de Google Cloud. La cual 
permite una configuracion rapida y sin mayores complicaciones.

```
🔔 Por motivos de simplicidad se escogio Google Cloud Functions para el procesamiento de datos, 
ya que en este punto se deberia considerar si es Data Streaming o  Batch Processing. Para el 
primero se podria utilizar Cloud Composer y para el segundo DataFlow.
```


## Parte 2: Aplicaciones y flujo CI/CD

### Arquitectura general.-

- **Publicación de Datos:** Los productores de datos (por ejemplo, dispositivos IoT, aplicaciones web) envían datos 
al tópico de Cloud Pub/Sub (_Data_).
- **Procesamiento de Datos:** Una Cloud Function está suscrita al tópico de Pub/Sub (Data) y se ejecuta cada vez que 
se publica un nuevo mensaje. Esta función procesa el mensaje y lo almacena en BigQuery.
- **Consulta y Exposición de Datos:** Los usuarios finales pueden hacer solicitudes HTTP a la API 
desplegada en Cloud Run. La API realiza consultas a BigQuery para recuperar los datos solicitados y 
los devuelve en la respuesta HTTP.


![img.png](img.png)

### Despliegue de la API
Para desplegar la API en Cloud Run utilizando el [pipeline](./build/cloudbuild.yaml) , se han
seguido los siguientes pasos:

- **Construcción de la imagen del contenedor:**
La API se empaqueta en una imagen de Docker utilizando un Dockerfile específico para FastAPI.
Esto crea un contenedor con el entorno necesario para ejecutar la API.

- **Subir la imagen a Container Registry:**
Una vez construida la [imagen](./build/FastAPI.Dockerfile), se sube al Container Registry de Google Cloud para 
su almacenamiento y posterior uso en el despliegue. 

- **Despliegue en Cloud Run:**
Se utiliza la imagen almacenada en el Container Registry para desplegar la API en Cloud Run.
En el despliegue se incluyen los detalles de configuracion como la región, el puerto (8000), 
los recursos asignados (2Gi de memoria, 1 CPU), y un mínimo de 1 instancia activa. Para esto se 
ultilizo _**gcloud cli**_, la cual es la linea de comandos proporcionada por GCP.


## Parte 3: Pruebas de Integración y Puntos Críticos de Calidad

### [Pruebas de integracion](./api/tests/test_api.py)
La API cuenta con solo dos rutas críticas:
```shell
1) /get_data/{action_id}:{user_email}
```
Se probo que, para un _action_id_ y un _user_email_ validos, la API devuelva un estado 200 OK con los datos correctos.
Se verifico que la lógica de la API maneja correctamente la ruta y devuelve los datos esperados en base a los parámetros proporcionados.

```shell
2) /app_info/{app_id}:{app_department}
```
Se probó que, cuando el usuario no está autenticado, la API devuelva el error esperado `(401 Unauthorized)`.
Se valido el mecanismo de autenticación, ya que esta ruta ejecuta una funcion que usa la API de Bigquery para obtener la informacion.

### Posibles Mejoras
Para robustecer la suite de pruebas en el futuro, se deberia incluir:

- Pruebas de carga y rendimiento, para asegurar que la API mantenga el desempeño bajo cargas elevadas.
- Pruebas de validación de datos, para verificar que la entrada de datos erróneos o maliciosos sea manejada 
correctamente por la API.


### Posibles Puntos Críticos en la Arquitectura

1. **Cloud Run - Latencia y Escalabilidad:**
Cloud Run escala automáticamente, pero puede generar latencia en el primer request 
(cold start) y tiene un límite de peticiones simultáneas por instancia. 
</br>
</br>
2. **Cloud Pub/Sub - Pérdida de Mensajes o Demoras:**
Si el sistema tiene problemas de procesamiento o Cloud Functions no puede procesar mensajes lo suficientemente rápido, 
los mensajes pueden acumularse, creando cuellos de botella.
</br>
</br>
3. **Cloud Functions - Sobrecarga y Fallos en el Procesamiento:**
Cloud Functions puede sobrecargarse si recibe demasiados mensajes al mismo tiempo o si el procesamiento 
de cada mensaje es demasiado lento.
</br>
</br>
4. **BigQuery - Performance de Consultas y Costos:**
Si las consultas a BigQuery son muy complejas o se ejecutan con demasiada frecuencia, esto puede generar 
altos costos y latencia significativa.
</br>
</br>
5. **Identity-Aware Proxy (IAP) - Autenticación y Acceso:**
Si la configuración de IAP no fue correctamente configurada, puede introducir latencias en la autenticación o posibles 
brechas de seguridad.

### Posibles Puntos de mejora en la Arquitectura

1. **Cloud Run**
Google Kubernetes Engine (GKE) es una buena alternativa que permite una escalabilidad controlada. 
A diferencia de Cloud Run, GKE permitiria un control más granular sobre cómo y cuándo escalar la API, 
sin depender tanto de las políticas automáticas de Cloud Run.
Los arranques en frío se minimizan cuando se tiene un mayor control sobre la infraestructura, se puede optimizar 
las configuraciones para reducir o eliminar el impacto de arranques en frío, manteniendo nodos y contenedores siempre listos.
</br>
</br>
2. **Cloud Pub/Sub**
Apache Kafka es una buena alternativa si se necesita manejar grandes volúmenes de datos en tiempo real. Su capacidad 
de procesamiento en tiempo real, y retención de mensajes más robusta la convierten en una alternativa ideal (Siempre 
y cuando se tengan grandes volumenes de datos).
</br>
</br>
3. **Cloud Functions**
DataFlow es una alternativa ideal cuando necesitas manejar grandes volúmenes de datos de manera continua (Streaming) o 
en lotes (Batch). Tiene integración con Pub/Sub y ofrece un procesamiento paralelo a gran escala.
Algunas de sus ventajas es el escalado automático, baja latencia en el procesamiento de datos en 
tiempo real.
</br>
</br>
4. **BigQuery**
Cloud Spanner es una base de datos relacional y distribuida. A diferencia de BigQuery, Cloud Spanner esta disenado para
tener una alta transaccionalidad, ademas de proporcionar los datos en tiempo real.
Si se tiene consultas muy frecuentes y menos analíticas, Cloud Spanner puede ser más económico que BigQuery 
porque no se basa en el modelo de "pago por tamano de Query"
</br>
</br>
5. **Identity-Aware Proxy (IAP)**
Para IAP se deberia tener en cuenta el uso de roles y permisos granulares. En otras palabras de debe asignar 
roles específicos con los permisos mínimos necesarios. De esta forma se puede mejorar la seguridad y reducir 
la posibilidad de un mal uso.

## Parte 4: Métricas y Monitoreo

- **Metricas adicionales**
1) **Latencia de Solicitudes de la API**</br>
La latencia de solicitudes de la API mide el tiempo que tarda en responder, y es clave para detectar
cuellos de botella en el procesamiento o acceso a datos. Yo utilizaria Google Cloud Monitoring ya que permite rastrear 
esta métrica y tomar acciones rápidas si la latencia supera ciertos umbrales.
</br>
</br>
2) **Cantidad de Mensajes recibidos en Cloud Pub/Sub**</br>
El número de mensajes procesados en Pub/Sub ayuda a identificar problemas en la ingesta y procesamiento de datos. 
Un alto numero de errores o reintentos puede señalar fallos de conectividad o saturacion en las Cloud Functions.
</br>
</br>
3) **Errores de la API**</br>
Finalmente, la tasa de errores de la API muestra el porcentaje de solicitudes fallidas `(4xx o 5xx)`. 
Incrementos en estos errores pueden ser síntomas de problemas de autenticación, permisos o errores de lógica, 
lo que puede ser fácilmente detectado y gestionado mediante Google Cloud Logging.

- **Herramienta de vizualizacion y monitoreo**
</br>
Google Cloud Monitoring es ideal para visualizar métricas como la latencia de la API, 
tasa de errores y mensajes procesados en Pub/Sub. Permite crear dashboards personalizados 
que ayudan a identificar cuellos de botella y fallos, optimizando el rendimiento. 
Su implementación en la nube es sencilla, ya que se integra con servicios como Cloud Run y BigQuery, 
recolectando métricas automáticamente. 
</br></br>
Al escalar a 50 sistemas, la visualización agregaría métricas de clúster y uso de red, 
pero la observabilidad podría complicarse si no se filtran adecuadamente, afectando la respuesta a incidentes 
y el rendimiento general.
</br></br>
La escalabilidad puede generar demasiadas metricas, dificultando su análisis si no se agrupan o filtran correctamente. 
Sin un monitoreo adecuado, podría ser difícil identificar problemas específicos.