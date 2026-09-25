"""Animación de una lista enlazada simple con Manim.

Muestra paso a paso: qué es una lista enlazada, insertar al inicio,
insertar al final, buscar y eliminar, y termina con la complejidad.
Al costado de cada operación aparece su código en C++ y se resalta
la línea que se está ejecutando en ese momento.

Ejecutar:  manim -pqh linked_list.py ListaEnlazada
"""
import textwrap

import numpy as np
from manim import *

# Autores
AUTOR_1 = "Francis Huerta Roque"
AUTOR_2 = "Saúl Baltazar Palomino"

# Medidas del dibujo
NODE_W = 1.4    # ancho de un nodo (valor + puntero)
GAP = 0.9       # separación horizontal entre nodos
NULL_W = 1.3    # ancho reservado para el texto nullptr
ROW_Y = 1.95    # altura de la fila principal de nodos
BAJADA = 1.55   # cuánto bajan los nodos nuevos o los que se eliminan

# Panel de código
FUENTE_CODIGO = "Monospace"   
TAM_CODIGO = 16

# Código C++ que se muestra al costado de cada operación
COD_NODO = """struct Nodo {
    int valor;
    Nodo* sig;
};
Nodo* head;"""

COD_INICIO = """void insertarInicio(int x) {
    Nodo* nuevo = new Nodo;
    nuevo->valor = x;
    nuevo->sig = head;
    head = nuevo;
}"""

COD_FINAL = """void insertarFinal(int x) {
    Nodo* nuevo = new Nodo;
    nuevo->valor = x;
    nuevo->sig = nullptr;
    if (head == nullptr) {
        head = nuevo;
        return;
    }
    Nodo* actual = head;
    while (actual->sig != nullptr)
        actual = actual->sig;
    actual->sig = nuevo;
}"""

COD_BUSCAR = """bool buscar(int x) {
    Nodo* actual = head;
    while (actual != nullptr) {
        if (actual->valor == x)
            return true;
        actual = actual->sig;
    }
    return false;
}"""

COD_ELIMINAR = """void eliminar(int x) {
    if (head->valor == x) {
        Nodo* borrar = head;
        head = head->sig;
        delete borrar;
        return;
    }
    Nodo* anterior = head;
    while (anterior->sig->valor != x)
        anterior = anterior->sig;
    Nodo* borrar = anterior->sig;
    anterior->sig = borrar->sig;
    delete borrar;
}"""


class ListaEnlazada(Scene):
    def construct(self):
        self.txt_titulo = None     # título de la sección actual
        self.txt_subtitulo = None  # explicación del paso actual
        self.codigo = None         # panel con el código C++ de la sección
        self.barra = None          # resaltado de la línea que se ejecuta
        self.nodos = []            # nodos de la lista, en orden

        self.intro()
        self.concepto()
        self.insertar_inicio(40)
        self.insertar_final(50)
        self.buscar(30)
        self.eliminar(20)
        self.complejidad()
        self.creditos()

    # ------------------------------------------------------------------
    # Textos y panel de código
    # ------------------------------------------------------------------
    def crear_titulo(self, texto):
        return Text(texto, font_size=38, color=BLUE_B).to_edge(UP, buff=0.3)

    def crear_panel(self, codigo):
        panel = Code(
            code_string=codigo, language="cpp", formatter_style="one-dark",
            add_line_numbers=False, background="rectangle",
            background_config={"buff": 0.2, "fill_color": "#161b22",
                               "stroke_color": GRAY_D, "stroke_width": 1.5,
                               "corner_radius": 0.15},
            paragraph_config={"font": FUENTE_CODIGO, "font_size": TAM_CODIGO,
                              "line_spacing": 0.45})
        if panel.height < 2.2:             # los códigos cortos se ven más grandes
            panel.scale(min(1.35, 2.2 / panel.height))
        panel.to_corner(DR, buff=0.2)
        # Recta y = origen + pendiente * i que da el centro vertical de la línea i
        ys = [linea.get_y() for linea in panel.code_lines]
        panel.pendiente, panel.origen = np.polyfit(range(len(ys)), ys, 1)
        return panel

    def seccion(self, texto, codigo):
        """Cambia el título, el panel de código y limpia la explicación anterior."""
        titulo = self.crear_titulo(texto)
        panel = self.crear_panel(codigo)
        anims = [FadeIn(titulo), FadeIn(panel, shift=LEFT * 0.3)]
        for viejo in (self.txt_titulo, self.txt_subtitulo, self.codigo, self.barra):
            if viejo is not None:
                anims.append(FadeOut(viejo))
        self.play(*anims, run_time=0.7)
        self.txt_titulo, self.codigo = titulo, panel
        self.txt_subtitulo = self.barra = None

    def resaltar(self, desde, hasta=None, color=YELLOW):
        """Animación que lleva el resaltado a las líneas [desde, hasta] del código."""
        hasta = desde if hasta is None else hasta
        p = self.codigo
        y = p.origen + p.pendiente * (desde + hasta) / 2
        alto = abs(p.pendiente) * (hasta - desde + 1)
        nueva = Rectangle(width=p.width - 0.16, height=alto, color=color,
                          stroke_width=1.5, fill_color=color, fill_opacity=0.2)
        nueva.move_to([p.get_x(), y, 0])
        if self.barra is None:
            self.barra = nueva
            return FadeIn(nueva)
        return Transform(self.barra, nueva)

    def subtitulo(self, texto, espera=1.0, resaltar=None, color=YELLOW):
        """Explicación del paso actual, abajo a la izquierda.

        `resaltar` es una línea del código o una tupla (desde, hasta).
        """
        nuevo = Text(textwrap.fill(texto, 44), font_size=26)
        if self.codigo is not None:
            ancho_max = self.codigo.get_left()[0] + config.frame_width / 2 - 0.9
            if nuevo.width > ancho_max:
                nuevo.scale_to_fit_width(ancho_max)
            nuevo.to_corner(DL, buff=0.5)
        else:
            nuevo.to_edge(DOWN, buff=0.5)
        anims = [FadeIn(nuevo)]
        if self.txt_subtitulo is not None:
            anims.append(FadeOut(self.txt_subtitulo))
        if resaltar is not None:
            desde, hasta = resaltar if isinstance(resaltar, tuple) else (resaltar, resaltar)
            anims.append(self.resaltar(desde, hasta, color))
        self.play(*anims, run_time=0.5)
        self.txt_subtitulo = nuevo
        self.wait(espera)

    def limpiar_escena(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.txt_titulo = self.txt_subtitulo = self.codigo = self.barra = None

    # ------------------------------------------------------------------
    # Nodos, flechas y posiciones
    # ------------------------------------------------------------------
    def crear_nodo(self, valor):
        dato = Rectangle(width=0.9, height=0.9, color=BLUE)
        ptr = Rectangle(width=0.5, height=0.9, color=BLUE).next_to(dato, RIGHT, buff=0)
        txt = Text(str(valor), font_size=30).move_to(dato)
        punto = Dot(radius=0.07, color=YELLOW).move_to(ptr)
        nodo = VGroup(dato, ptr, txt, punto)   # índices: 0 valor, 1 puntero, 2 texto, 3 punto
        nodo.valor = valor
        nodo.sig = None            # nodo al que apunta (None = nullptr)
        nodo.flecha_sal = None     # flecha que sale de este nodo
        return nodo

    def flecha(self, inicio, fin, color=YELLOW):
        return Arrow(inicio, fin, buff=0, color=color, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3)

    def destino_de(self, nodo):
        """Punto al que llega una flecha: el borde izquierdo del nodo o de nullptr."""
        return self.nulo.get_left() if nodo is None else nodo[0].get_left()

    def vincular(self, nodo):
        """La flecha del nodo sigue automáticamente a sus extremos."""
        nodo.flecha_sal.add_updater(
            lambda m, n=nodo: m.put_start_and_end_on(
                n[3].get_center(), self.destino_de(n.sig)))

    def vincular_cabeza(self):
        self.flecha_cabeza.add_updater(
            lambda m: m.put_start_and_end_on(
                self.etiqueta_cabeza.get_bottom(), self.cabeza.get_top()))

    def re_enlazar(self, nodo, destino):
        """Cambia a dónde apunta `nodo`, animando la flecha."""
        nodo.flecha_sal.clear_updaters()
        nodo.sig = destino
        nueva = self.flecha(nodo[3].get_center(), self.destino_de(destino))
        self.play(Transform(nodo.flecha_sal, nueva))
        self.vincular(nodo)

    def re_enlazar_cabeza(self, nodo):
        self.flecha_cabeza.clear_updaters()
        self.cabeza = nodo
        nueva = self.flecha(self.etiqueta_cabeza.get_bottom(), nodo.get_top(), GREEN)
        self.play(Transform(self.flecha_cabeza, nueva))
        self.vincular_cabeza()

    def casilla_x(self, i, count):
        total = count * (NODE_W + GAP) + NULL_W
        return -total / 2 + i * (NODE_W + GAP) + NODE_W / 2

    def nulo_x(self, count):
        total = count * (NODE_W + GAP) + NULL_W
        return -total / 2 + count * (NODE_W + GAP) + NULL_W / 2

    def acomodar(self, count=None, offset=0):
        """Animaciones que acomodan los nodos actuales en sus casillas.

        `count` reserva casillas para nodos que aún no existen y `offset`
        deja libres las primeras casillas (para insertar allí después).
        """
        count = len(self.nodos) if count is None else count
        anims = [nd.animate.move_to([self.casilla_x(i + offset, count), ROW_Y, 0])
                 for i, nd in enumerate(self.nodos)]
        anims.append(self.nulo.animate.move_to([self.nulo_x(count), ROW_Y, 0]))
        anims.append(self.etiqueta_cabeza.animate.move_to(
            [self.casilla_x(0, count), ROW_Y + 1.05, 0]))
        return anims

    def armar_lista(self, valores):
        n = len(valores)
        self.nodos = [self.crear_nodo(v) for v in valores]
        for i, nd in enumerate(self.nodos):
            nd.move_to([self.casilla_x(i, n), ROW_Y, 0])
        self.nulo = Text("nullptr", font_size=26, color=RED_B).move_to(
            [self.nulo_x(n), ROW_Y, 0])
        self.etiqueta_cabeza = Text("head", font_size=24, color=GREEN).move_to(
            [self.casilla_x(0, n), ROW_Y + 1.05, 0])
        for i, nd in enumerate(self.nodos):
            nd.sig = self.nodos[i + 1] if i + 1 < n else None
            nd.flecha_sal = self.flecha(nd[3].get_center(), self.destino_de(nd.sig))
        self.cabeza = self.nodos[0]
        self.flecha_cabeza = self.flecha(
            self.etiqueta_cabeza.get_bottom(), self.cabeza.get_top(), GREEN)

        self.play(LaggedStart(*[FadeIn(nd, shift=UP * 0.3) for nd in self.nodos],
                              lag_ratio=0.4))
        self.play(FadeIn(self.nulo), *[Create(nd.flecha_sal) for nd in self.nodos])
        self.play(FadeIn(self.etiqueta_cabeza), Create(self.flecha_cabeza))
        for nd in self.nodos:
            self.vincular(nd)
        self.vincular_cabeza()

    def crear_cursor(self, nodo, texto="actual", color=ORANGE):
        flecha = Arrow(DOWN * 0.7, ORIGIN, buff=0, color=color, stroke_width=4)
        txt = Text(texto, font_size=22, color=color).next_to(flecha, DOWN, buff=0.05)
        return VGroup(flecha, txt).next_to(nodo, DOWN, buff=0.1)

    def recorrer(self, hasta, mensaje=None, linea_visita=None, linea_avance=None):
        """El puntero `actual` camina desde head hasta el nodo `hasta`.

        `linea_visita` se resalta al revisar cada nodo y `linea_avance`
        cuando el puntero salta al siguiente.
        """
        cursor = self.crear_cursor(self.nodos[0])
        self.play(FadeIn(cursor))
        for i in range(hasta + 1):
            nd = self.nodos[i]
            if i > 0:
                anims = [cursor.animate.next_to(nd, DOWN, buff=0.1)]
                if linea_avance is not None:
                    anims.append(self.resaltar(linea_avance))
                self.play(*anims, run_time=0.6)
            anims = [nd[0].animate.set_fill(ORANGE, opacity=0.4)]
            if linea_visita is not None:
                anims.append(self.resaltar(linea_visita))
            self.play(*anims, run_time=0.4)
            if mensaje:
                self.subtitulo(mensaje(nd, i == hasta), espera=0.5)
        return cursor

    def limpiar_recorrido(self, cursor):
        self.play(FadeOut(cursor),
                  *[nd[0].animate.set_fill(opacity=0) for nd in self.nodos],
                  run_time=0.5)

    # ------------------------------------------------------------------
    # Secciones del video
    # ------------------------------------------------------------------
    def intro(self):
        titulo = Text("Listas Enlazadas", font_size=64, color=BLUE_B)
        sub = Text("Animación con Manim · CS2023 Algoritmos y Estructuras de Datos",
                   font_size=24)
        autores = Text(f"{AUTOR_1}  ·  {AUTOR_2}", font_size=30)
        grupo = VGroup(titulo, sub, autores).arrange(DOWN, buff=0.5)
        self.play(Write(titulo))
        self.play(FadeIn(sub), FadeIn(autores))
        self.wait(2)
        self.play(FadeOut(grupo))

    def concepto(self):
        self.seccion("¿Qué es una lista enlazada?", COD_NODO)
        self.subtitulo("Es una secuencia de nodos conectados por punteros")
        self.armar_lista([10, 20, 30])

        primero = self.nodos[0]
        lbl_valor = Text("valor", font_size=22, color=BLUE_B)
        lbl_valor.next_to(primero[0], DOWN, buff=0.2)
        lbl_sig = Text("sig", font_size=22, color=YELLOW)
        lbl_sig.next_to(primero[1], DOWN, buff=0.2)
        self.subtitulo("Cada nodo guarda un valor y un puntero al siguiente nodo", espera=0.3)
        self.play(FadeIn(lbl_valor), self.resaltar(1), run_time=0.6)
        self.wait(0.6)
        self.play(FadeIn(lbl_sig), self.resaltar(2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(lbl_valor), FadeOut(lbl_sig))

        self.subtitulo("El último apunta a nullptr y head apunta al primero",
                       espera=0.3, resaltar=4)
        self.play(Indicate(self.nulo), Indicate(self.etiqueta_cabeza))
        self.wait(1)

    def insertar_inicio(self, valor):
        self.seccion("Insertar al inicio  ·  O(1)", COD_INICIO)
        n = len(self.nodos)

        self.subtitulo(f"1. Creamos el nodo nuevo con valor {valor}",
                       espera=0.3, resaltar=(1, 2))
        nuevo = self.crear_nodo(valor)
        nuevo.move_to([self.casilla_x(0, n + 1), ROW_Y - BAJADA, 0])
        self.play(*self.acomodar(n + 1, offset=1))
        self.play(FadeIn(nuevo, shift=UP * 0.3))

        self.subtitulo("2. Su sig apunta al antiguo head", espera=0.3, resaltar=3)
        nuevo.sig = self.cabeza
        nuevo.flecha_sal = self.flecha(nuevo[3].get_center(), self.destino_de(self.cabeza))
        self.play(Create(nuevo.flecha_sal))
        self.vincular(nuevo)

        self.subtitulo("3. head pasa a apuntar al nuevo nodo", espera=0.3, resaltar=4)
        self.re_enlazar_cabeza(nuevo)

        self.subtitulo("Solo cambiamos dos punteros: no importa el tamaño de la lista",
                       espera=0.3, resaltar=(3, 4))
        self.nodos.insert(0, nuevo)
        self.play(*self.acomodar())
        self.wait(1)

    def insertar_final(self, valor):
        self.seccion("Insertar al final  ·  O(n)", COD_FINAL)
        n = len(self.nodos)

        self.subtitulo(f"1. Creamos el nodo nuevo ({valor}) con sig = nullptr",
                       espera=0.3, resaltar=(1, 3))
        nuevo = self.crear_nodo(valor)
        nuevo.move_to([self.casilla_x(n, n + 1), ROW_Y - BAJADA, 0])
        self.play(*self.acomodar(n + 1))
        self.play(FadeIn(nuevo, shift=UP * 0.3))
        nuevo.flecha_sal = self.flecha(nuevo[3].get_center(), self.destino_de(None))
        self.play(Create(nuevo.flecha_sal))
        self.vincular(nuevo)

        self.subtitulo("¿La lista está vacía? No: hay que buscar el último",
                       espera=0.5, resaltar=4)
        self.subtitulo("2. actual recorre la lista desde head", espera=0.3, resaltar=8)

        def mensaje(nd, ultimo):
            if ultimo:
                return "actual->sig es nullptr: es el último"
            return "actual->sig no es nullptr: avanzamos"

        cursor = self.recorrer(n - 1, mensaje, linea_visita=9, linea_avance=10)

        self.subtitulo("3. El último nodo apunta al nuevo", espera=0.3, resaltar=11)
        self.re_enlazar(self.nodos[-1], nuevo)
        self.limpiar_recorrido(cursor)
        self.nodos.append(nuevo)
        self.play(*self.acomodar())
        self.wait(1)

    def buscar(self, valor):
        self.seccion("Buscar  ·  O(n)", COD_BUSCAR)
        idx = next(i for i, nd in enumerate(self.nodos) if nd.valor == valor)

        self.subtitulo(f"Buscamos x = {valor}: actual parte desde head",
                       espera=0.3, resaltar=1)

        def mensaje(nd, ultimo):
            return f"¿{nd.valor} = {valor}?  " + (
                "Sí: ¡lo encontramos!" if ultimo else "No: avanzamos")

        cursor = self.recorrer(idx, mensaje, linea_visita=3, linea_avance=5)
        self.play(self.nodos[idx][0].animate.set_fill(GREEN, opacity=0.6),
                  self.resaltar(4, color=GREEN))
        self.wait(0.5)
        self.subtitulo("En el peor caso recorremos toda la lista: O(n)",
                       espera=1.5, resaltar=(2, 6))
        self.limpiar_recorrido(cursor)

    def eliminar(self, valor):
        self.seccion("Eliminar un nodo  ·  O(n)", COD_ELIMINAR)
        idx = next(i for i, nd in enumerate(self.nodos) if nd.valor == valor)
        objetivo = self.nodos[idx]
        primero = self.nodos[0]

        if idx == 0:
            # Caso especial: x está en head, que no tiene nodo anterior
            self.subtitulo(f"¿x está en head? Sí: {valor} no tiene anterior",
                           espera=0.3, resaltar=1, color=GREEN)
            self.play(Indicate(primero, color=GREEN))

            self.subtitulo("1. Guardar: borrar = head", espera=0.3, resaltar=2)
            borrar = self.crear_cursor(objetivo, "borrar", RED)
            self.play(FadeIn(borrar))

            self.subtitulo("2. Reconectar: head = head->sig", espera=0.3, resaltar=3)
            self.play(objetivo.animate.shift(DOWN * BAJADA).set_color(RED),
                      borrar.animate.shift(DOWN * BAJADA))
            self.re_enlazar_cabeza(objetivo.sig)
            restos = []
            paso_delete, linea_delete = 3, 4
        else:
            # Caso general: anterior se detiene justo antes del nodo a borrar
            self.subtitulo(f"¿x está en head? {primero.valor} ≠ {valor}: no",
                           espera=0.3, resaltar=1)
            self.play(Indicate(primero))

            self.subtitulo("1. anterior camina hasta quedar justo antes de x",
                           espera=0.3, resaltar=7)
            anterior = self.crear_cursor(primero, "anterior", TEAL)
            self.play(FadeIn(anterior))
            for i in range(idx):
                siguiente = self.nodos[i + 1]
                es_x = (i + 1 == idx)
                self.play(siguiente[0].animate.set_fill(ORANGE, opacity=0.4),
                          self.resaltar(8), run_time=0.4)
                self.subtitulo(f"anterior->sig vale {siguiente.valor}: " + (
                    "es x, paramos" if es_x else f"≠ {valor}, avanzamos"), espera=0.5)
                if not es_x:
                    self.play(anterior.animate.next_to(siguiente, DOWN, buff=0.1),
                              siguiente[0].animate.set_fill(opacity=0),
                              self.resaltar(9), run_time=0.6)
            previo = self.nodos[idx - 1]

            self.subtitulo("2. Guardar: borrar = anterior->sig", espera=0.3, resaltar=10)
            borrar = self.crear_cursor(objetivo, "borrar", RED)
            self.play(FadeIn(borrar))

            self.subtitulo("3. Reconectar: anterior->sig = borrar->sig",
                           espera=0.3, resaltar=11)
            self.play(objetivo.animate.shift(DOWN * BAJADA).set_color(RED),
                      borrar.animate.shift(DOWN * BAJADA))
            self.re_enlazar(previo, objetivo.sig)
            restos = [FadeOut(anterior)]
            paso_delete, linea_delete = 4, 12

        self.subtitulo(f"{paso_delete}. delete borrar: liberamos su memoria",
                       espera=0.3, resaltar=linea_delete, color=RED)
        objetivo.flecha_sal.clear_updaters()
        self.play(FadeOut(objetivo), FadeOut(objetivo.flecha_sal), FadeOut(borrar), *restos)
        self.nodos.remove(objetivo)
        self.play(*self.acomodar())

        if idx == 0:
            self.subtitulo("Si x está en head no hay que buscar: O(1)",
                           espera=1.2, resaltar=(1, 5))
        else:
            self.subtitulo("Reconectar es O(1): lo que cuesta es buscar, O(n)",
                           espera=1.2, resaltar=(8, 9))

    def complejidad(self):
        self.limpiar_escena()
        titulo = self.crear_titulo("Complejidad de las operaciones")
        self.play(FadeIn(titulo))
        filas = [["Operación", "Tiempo"],
                 ["Insertar al inicio", "O(1)"],
                 ["Insertar al final (sin puntero tail)", "O(n)"],
                 ["Buscar", "O(n)"],
                 ["Eliminar (buscando el nodo)", "O(n)"]]
        tabla = Table(filas, include_outer_lines=True,
                      element_to_mobject=lambda s: Text(s, font_size=28)).scale(0.9)
        self.play(tabla.create(), run_time=2)
        self.wait(4)

    def creditos(self):
        self.limpiar_escena()
        gracias = Text("¡Gracias!", font_size=60, color=BLUE_B)
        autores = Text(f"{AUTOR_1}  ·  {AUTOR_2}", font_size=30)
        hecho = Text("Hecho con Manim Community", font_size=22, color=GRAY)
        grupo = VGroup(gracias, autores, hecho).arrange(DOWN, buff=0.5)
        self.play(FadeIn(grupo))
        self.wait(3)
        self.play(FadeOut(grupo))
