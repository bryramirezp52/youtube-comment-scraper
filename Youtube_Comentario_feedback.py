import requests
import json
import html
from pathlib import Path
from datetime import datetime
import re

# Carpeta donde se guardarán los informes
directorio_informes = r"C:\Users\Nebula\Informes Youtube"

# Función para limpiar texto y entidades HTML
def limpiar(texto):
    if texto is None:
        return ""
    texto_str = str(texto)
    texto_unescaped = html.unescape(texto_str)
    return texto_unescaped.replace("â˜…", "★")

# Genera ruta con timestamp en la carpeta de informes
def generar_ruta_salida() -> Path:
    carpeta = Path(directorio_informes)
    carpeta.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return carpeta / f"comentarios_{timestamp}.txt"

# Escribe el texto en el archivo indicado
def escribir_resultado(path: Path, texto: str):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)

# Función principal: envía la URL al webhook, procesa y guarda los comentarios numerados
def analizar_video(video_url, webhook_url) -> bool:
    # Validación de la URL
    if not re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/", video_url, re.I):
        print("⚠️ La URL no parece ser de YouTube. Intenta de nuevo.")
        return False

    payload = {"videoUrl": video_url}
    print("\n⏳ Obteniendo comentarios... Espere por favor.")

    try:
        response = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=120
        )
        response.encoding = "utf-8"
        response.raise_for_status()
        data_respuesta = response.json()

        # Extraer la carga útil de comentarios (puede ser dict, list o lista con dict)
        if isinstance(data_respuesta, dict):
            contenido = data_respuesta.get("content") or \
                        data_respuesta.get("message", {}).get("content") or \
                        data_respuesta
        else:
            contenido = data_respuesta

        # Intentar parsear si viene como string JSON
        if isinstance(contenido, str):
            try:
                contenido = json.loads(contenido)
            except json.JSONDecodeError:
                pass

        # Normalizar lista de comentarios
        if isinstance(contenido, dict) and isinstance(contenido.get("comments"), list):
            comentarios = contenido["comments"]
        elif isinstance(contenido, list):
            # caso: [ { "comments": [...] } ]
            if len(contenido) == 1 and isinstance(contenido[0], dict) and isinstance(contenido[0].get("comments"), list):
                comentarios = contenido[0]["comments"]
            else:
                comentarios = contenido
        else:
            comentarios = [contenido]

        # Construir lista numerada y añadir total al final
        lineas = []
        for i, comentario in enumerate(comentarios, start=1):
            texto = limpiar(comentario)
            lineas.append(f"{i}. {texto}")
        lineas.append(f"\nTotal de comentarios: {len(comentarios)}")

        resultado = "\n".join(lineas)

        # Guardar en archivo
        ruta = generar_ruta_salida()
        escribir_resultado(ruta, resultado)
        print(f"✅ {len(comentarios)} comentarios guardados en: {ruta.resolve()}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    webhook = "http://localhost:5678/webhook/youtube-comments"
    while True:
        url = input("➡️ URL de YouTube (o 'salir'): ").strip()
        if url.lower() == "salir":
            break
        if url:
            analizar_video(url, webhook)
            print("-" * 30)

    print("👋 Fin de sesión.")
