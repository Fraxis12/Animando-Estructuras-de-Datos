# Listas Enlazadas animadas con Manim

Proyecto 1 de **CS2023 - Algoritmos y Estructuras de Datos** (UTEC).
Autores: Francis Huerta Roque y Saúl Baltazar Palomino.

Video animado que muestra cómo funciona una **lista enlazada simple**: insertar al inicio, insertar al final, buscar y eliminar. Mientras se anima cada operación, al costado aparece su código en C++ con la línea que se ejecuta resaltada.

🎬 **Video demo:** _(pegar link)_

## Requisitos

- Python 3.9 o superior
- Las librerías de `requirements.txt` (Manim Community)

No se necesita LaTeX.

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

## Estructura del repositorio

```
linked_list.py     # toda la animación (escena ListaEnlazada)
requirements.txt   # dependencias de Python
README.md
```

## Personalizar

Al inicio de `linked_list.py`:

- `AUTOR_1`, `AUTOR_2`: nombres que aparecen en el video.
- `TAM_CODIGO`: tamaño de la letra del panel de código.
- `FUENTE_CODIGO`: fuente del panel. En Windows, si se ve delgada, cambiar `"Monospace"` por `"Consolas"`.
