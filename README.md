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

```
🔔 Por motivos de simplicidad se escogio Google Cloud Functions para el procesamiento de datos, ya que 
en este punto se deberia considerar si es Data Streaming o  Batch Processing. Para el primero se podria utilizar 
Cloud Composer y para el segundo DataFlow.
```

## Arquitectura general.-

![img.png](img.png)

[//]: # (```mermaid)

[//]: # (flowchart TD)

[//]: # (    A&#40;[Productores de datos </br> Apps o Dispositivos IoT]&#41; -->|Publicación de mensajes| B[Cloud Pub/Sub Topic];)

[//]: # (    B --> C[Cloud Function];)

[//]: # (    C --> D[&#40;BigQuery&#41;];)

[//]: # (    E&#40;&#40;Usuario Final&#41;&#41; -->|Solicitud HTTP| F[API en Cloud Run];)

[//]: # (    F -->|Consulta| D;)

[//]: # (    D -->|Datos| F;)

[//]: # (    F -->|Respuesta HTTP| E;)

[//]: # (```)






