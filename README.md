# YouTube Comment Scraper y Analizador

![YouTube Comment Scraper](/imagenes/YouTube%20Comment%20Scraper.png)

## Descripción General

Este proyecto ofrece una solución automatizada para extraer comentarios de videos de YouTube y guardarlos en un formato legible. Combina un flujo de trabajo de automatización en `n8n` para la recolección de datos mediante la API de YouTube y un script en Python para la interacción con el webhook, el procesamiento de la respuesta y el almacenamiento local de los comentarios.

Ideal para creadores de contenido, investigadores de mercado o cualquier persona interesada en analizar el feedback de la audiencia de YouTube de forma programática.

## Componentes del Proyecto

1.  **Workflow n8n (`Youtube_Comment_Feedback_1000_con_Webhook.json`):**
    * **Webhook:** Punto de entrada para iniciar el proceso de extracción, recibiendo la URL del video.
    * **Procesar: Extraer Video ID:** Un nodo de código JavaScript que parsea la `videoUrl` proporcionada y extrae el `videoId` necesario para la API de YouTube.
    * **API YouTube: Obtener Comentarios (paginar):** Realiza solicitudes a la API de YouTube (`commentThreads`) para obtener comentarios, manejando la paginación para recolectar hasta 1000 comentarios por video (limitado a 10 requests de 100 resultados cada uno).
    * **Limpiar y Unificar Comentarios:** Otro nodo de código JavaScript que procesa la respuesta de la API, limpia el texto de los comentarios (eliminando HTML y espacios extra) y unifica los comentarios en un array, eliminando duplicados.
    * **Respond to Webhook:** Envía los comentarios procesados de vuelta al script de Python.

2.  **Script Python (`Youtube_Comentario_feedback.py`):**
    * **Interacción con Webhook:** Envía la URL del video al webhook de n8n.
    * **Manejo de Respuesta:** Recibe y procesa la respuesta del webhook, extrayendo la lista de comentarios.
    * **Limpieza y Formato:** Asegura que los comentarios estén limpios de caracteres HTML y formateados para su visualización.
    * **Guardado Local:** Almacena los comentarios numerados, junto con un recuento total, en un archivo de texto (`.txt`) con un timestamp en una carpeta configurable (`C:\Users\Nebula\Informes Youtube`).

## Cómo Usar

### Prerrequisitos

* **n8n:** Instancia local o en la nube de n8n configurada y en ejecución.
* **Clave de API de YouTube:** Una clave de API de Google Cloud Platform con acceso habilitado a la API de Datos de YouTube v3.
* **Python 3.x:** Entorno de Python configurado.
* **Librerías Python:** `requests`, `json`, `html`, `pathlib`, `datetime`, `re`.

### Configuración

1.  **n8n Workflow:**
    * Importa el archivo `Youtube_Comment_Feedback_1000_con_Webhook.json` en tu instancia de n8n.
    * En el nodo "API YouTube: Obtener Comentarios (paginar)", reemplaza `AIzaSyD6s33ouosn6CtbzKMov22PkwTtwzE1Q6Y` con tu propia Clave de API de YouTube.
    * Activa el workflow.
    * Copia la URL del Webhook del nodo "Webhook".

2.  **Python Script:**
    * Abre `Youtube_Comentario_feedback.py`.
    * Actualiza la variable `webhook` con la URL del webhook de n8n que copiaste.
    * (Opcional) Modifica `directorio_informes` a la ruta donde deseas guardar los archivos de comentarios.

### Ejecución

1.  Asegúrate de que tu workflow de n8n esté activo.
2.  Ejecuta el script de Python desde tu terminal:
    ```bash
    python Youtube_Comentario_feedback.py
    ```
3.  El script te pedirá que ingreses la URL del video de YouTube que deseas analizar.

## Futuras Mejoras

* Implementar un análisis de sentimientos básico sobre los comentarios.
* Soporte para más de 1000 comentarios o para videos con un volumen extremadamente alto.
* Interfaz de usuario simple (GUI) para el script de Python.
* Exportación a otros formatos (CSV, JSON).
* Manejo de errores más robusto y reintentos.

## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejoras o encuentras algún problema, por favor abre un 'issue' o envía un 'pull request'.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
