# Listas Enlazadas animadas con Manim

Proyecto 1 de **CS2023 - Algoritmos y Estructuras de Datos**.
Autores: Francis Huerta Roque & Saúl Baltazar Palomino.

Video animado que muestra cómo funciona una **lista enlazada simple**: insertar al inicio, insertar al final, buscar y eliminar. Mientras se anima cada operación, al costado aparece su código en C++ con la línea que se ejecuta resaltada.

 **Video demo (con narración):** _https://drive.google.com/file/d/1grrLY2KJRfLTSAXFNBSluY9s-s0uEPfg/view_

> El video que genera Manim no tiene audio. La narración, hecha con una voz de IA, se agregó en la edición final; la versión narrada es la del link.

## Requisitos

- Python 3.9 o superior
- Las librerías de `requirements.txt` (Manim Community)


## Instalación y ejecución

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m manim -pqh linked_list.py ListaEnlazada
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
manim -pqh linked_list.py ListaEnlazada
```

En Linux, si la instalación falla, primero instala `libcairo2-dev libpango1.0-dev pkg-config`.

## Calidad del video

| Opción | Resolución | Uso | El video queda en |
|---|---|---|---|
| `-pql` | 480p, 15 fps | Vista previa rápida | `media/videos/linked_list/480p15/` |
| `-pqh` | 1080p, 60 fps | Versión final | `media/videos/linked_list/1080p60/` |

La `p` abre el video al terminar de compilar.
