# Animando Estructuras de Datos: Listas Enlazadas

Proyecto 1 del curso **CS2023 - Algoritmos y Estructuras de Datos**.

Animación hecha con [Manim Community](https://www.manim.community/) que explica, paso a paso,
cómo funciona una **lista enlazada simple**: qué es, cómo se inserta (al inicio y al final),
cómo se busca un valor, cómo se elimina un nodo y cuál es la complejidad de cada operación.

**Autores:** Nombre Apellido 1, Nombre Apellido 2

**Video demo:** _(agregar enlace)_

## Software requerido

- Python 3.9 o superior
- [Manim Community](https://docs.manim.community/en/stable/installation.html) (≥ 0.19)
- FFmpeg
- Cairo y Pango (dependencias de Manim). No se necesita LaTeX: el video solo usa `Text`.

## Instalación

Con pip (en Ubuntu/Debian primero instalar `libcairo2-dev libpango1.0-dev pkg-config ffmpeg`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

O con conda, que ya trae las dependencias de sistema:

```bash
conda create -n manim -c conda-forge python=3.12 manim ffmpeg
conda activate manim
```

## Cómo compilarlo y ejecutarlo

Manim genera el video al renderizar la escena `ListaEnlazada` de [linked_list.py](linked_list.py):

```bash
# Vista previa rápida (480p15)
manim -pql linked_list.py ListaEnlazada

# Alta resolución (1080p60, mp4) para la entrega
manim -pqh linked_list.py ListaEnlazada
```

El video queda en `media/videos/linked_list/1080p60/ListaEnlazada.mp4`.
Para poner los nombres de los autores, editar `AUTOR_1` y `AUTOR_2` al inicio de `linked_list.py`.

## La estructura: lista enlazada simple

Una lista enlazada es una secuencia de **nodos**. Cada nodo guarda un **dato** y un
**puntero al siguiente nodo**; el último apunta a `NULL`, y un puntero llamado **cabeza**
señala el primer nodo. A diferencia de un arreglo, los nodos no están contiguos en memoria,
así que insertar o eliminar solo requiere cambiar punteros, sin desplazar elementos.

| Operación                              | Tiempo |
|----------------------------------------|--------|
| Insertar al inicio                     | O(1)   |
| Insertar al final (sin puntero a cola) | O(n)   |
| Buscar                                 | O(n)   |
| Eliminar (buscando el nodo)            | O(n)   |

## Contenido del video (~90 s)

1. Título y autores
2. Qué es una lista enlazada
3. Insertar al inicio
4. Insertar al final
5. Buscar un valor
6. Eliminar un nodo
7. Tabla de complejidad y créditos
