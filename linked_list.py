"""Animación de una lista enlazada simple con Manim.

Muestra paso a paso: qué es una lista enlazada, insertar al inicio,
insertar al final, buscar y eliminar, y termina con la complejidad.

Ejecutar:  manim -pqh linked_list.py ListaEnlazada
"""
from manim import *

# Autores
AUTOR_1 = "Nombre Apellido 1"
AUTOR_2 = "Nombre Apellido 2"

# Medidas del dibujo
NODE_W = 1.4    # ancho de un nodo (dato + puntero)
GAP = 0.9       # separación horizontal entre nodos
NULL_W = 0.9    # ancho reservado para el texto NULL
ROW_Y = 0.6     # altura de la fila principal de nodos


class ListaEnlazada(Scene):
    def construct(self):
        self.txt_titulo = None     # título de la sección actual
        self.txt_subtitulo = None  # explicación del paso actual
        self.nodos = []            # nodos de la lista, en orden

        self.intro()
        self.concepto()
        self.insertar_inicio(40)
        self.insertar_final(50)
        self.buscar(30)
        self.eliminar(20)
        self.complejidad()
        self.creditos()

    def titulo(self, texto):
        nuevo = Text(texto, font_size=38, color=BLUE_B).to_edge(UP, buff=0.4)
        if self.txt_titulo is None:
            self.play(FadeIn(nuevo))
        else:
            self.play(FadeOut(self.txt_titulo), FadeIn(nuevo), run_time=0.6)
        self.txt_titulo = nuevo

    def subtitulo(self, texto, espera=1.0):
        nuevo = Text(texto, font_size=28).to_edge(DOWN, buff=0.5)
        if self.txt_subtitulo is None:
            self.play(FadeIn(nuevo, shift=UP * 0.2), run_time=0.5)
        else:
            self.play(FadeOut(self.txt_subtitulo), FadeIn(nuevo), run_time=0.5)
        self.txt_subtitulo = nuevo
        self.wait(espera)

    def limpiar_escena(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.txt_titulo = None
        self.txt_subtitulo = None

    def crear_nodo(self, valor):
        dato = Rectangle(width=0.9, height=0.9, color=BLUE)
        ptr = Rectangle(width=0.5, height=0.9, color=BLUE).next_to(dato, RIGHT, buff=0)
        txt = Text(str(valor), font_size=30).move_to(dato)
        punto = Dot(radius=0.07, color=YELLOW).move_to(ptr)
        nodo = VGroup(dato, ptr, txt, punto)   # índices: 0 dato, 1 puntero, 2 texto, 3 punto
        nodo.valor = valor
        nodo.sig = None           # nodo al que apunta (None = NULL)
        nodo.flecha_sal = None     # flecha que sale de este nodo
        return nodo

    def flecha(self, inicio, fin, color=YELLOW):
        return Arrow(inicio, fin, buff=0, color=color, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3)

    def destino_de(self, nodo):
        """Punto al que llega una flecha: el borde izquierdo del nodo o de NULL."""
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
            [self.casilla_x(0, count), ROW_Y + 1.5, 0]))
        return anims

    def armar_lista(self, valores):
        n = len(valores)
        self.nodos = [self.crear_nodo(v) for v in valores]
        for i, nd in enumerate(self.nodos):
            nd.move_to([self.casilla_x(i, n), ROW_Y, 0])
        self.nulo = Text("NULL", font_size=28, color=RED_B).move_to(
            [self.nulo_x(n), ROW_Y, 0])
        self.etiqueta_cabeza = Text("cabeza", font_size=24, color=GREEN).move_to(
            [self.casilla_x(0, n), ROW_Y + 1.5, 0])
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

    def crear_cursor(self, nodo):
        flecha = Arrow(DOWN * 0.7, ORIGIN, buff=0, color=ORANGE, stroke_width=4)
        txt = Text("actual", font_size=22, color=ORANGE).next_to(flecha, DOWN, buff=0.05)
        return VGroup(flecha, txt).next_to(nodo, DOWN, buff=0.1)

    def recorrer(self, hasta, mensaje=None):
        cursor = self.crear_cursor(self.nodos[0])
        self.play(FadeIn(cursor))
        for i in range(hasta + 1):
            nd = self.nodos[i]
            if i > 0:
                self.play(cursor.animate.next_to(nd, DOWN, buff=0.1), run_time=0.6)
            self.play(nd[0].animate.set_fill(ORANGE, opacity=0.4), run_time=0.3)
            if mensaje:
                self.subtitulo(mensaje(nd, i == hasta), espera=0.4)
        return cursor

    def limpiar_recorrido(self, cursor):
        self.play(FadeOut(cursor),
                  *[nd[0].animate.set_fill(opacity=0) for nd in self.nodos],
                  run_time=0.5)

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
        self.titulo("¿Qué es una lista enlazada?")
        self.subtitulo("Es una secuencia de nodos conectados por punteros")
        self.armar_lista([10, 20, 30])

        primero = self.nodos[0]
        dato = Text("dato", font_size=22, color=BLUE_B)
        dato.next_to(primero[0], DOWN, buff=0.2).shift(LEFT * 0.15)
        lbl_sig = Text("siguiente", font_size=22, color=YELLOW)
        lbl_sig.next_to(primero[1], DOWN, buff=0.2).shift(RIGHT * 0.35)
        self.subtitulo("Cada nodo guarda un dato y un puntero al siguiente nodo", espera=0.3)
        self.play(FadeIn(dato), FadeIn(lbl_sig))
        self.wait(1.5)
        self.play(FadeOut(dato), FadeOut(lbl_sig))

        self.subtitulo("El último apunta a NULL y la cabeza apunta al primero", espera=0.3)
        self.play(Indicate(self.nulo), Indicate(self.etiqueta_cabeza))
        self.wait(1)

    def insertar_inicio(self, valor):
        self.titulo("Insertar al inicio  ·  O(1)")
        n = len(self.nodos)

        self.subtitulo(f"1. Hacemos espacio y creamos el nodo nuevo ({valor})", espera=0.3)
        nuevo = self.crear_nodo(valor)
        nuevo.move_to([self.casilla_x(0, n + 1), ROW_Y - 1.9, 0])
        self.play(*self.acomodar(n + 1, offset=1))
        self.play(FadeIn(nuevo, shift=UP * 0.3))

        self.subtitulo("2. Su siguiente apunta a la antigua cabeza", espera=0.3)
        nuevo.sig = self.cabeza
        nuevo.flecha_sal = self.flecha(nuevo[3].get_center(), self.destino_de(self.cabeza))
        self.play(Create(nuevo.flecha_sal))
        self.vincular(nuevo)

        self.subtitulo("3. La cabeza pasa a apuntar al nuevo nodo", espera=0.3)
        self.re_enlazar_cabeza(nuevo)

        self.subtitulo("4. Solo cambiamos dos punteros: no importa el tamaño de la lista", espera=0.3)
        self.nodos.insert(0, nuevo)
        self.play(*self.acomodar())
        self.wait(1)

    def insertar_final(self, valor):
        self.titulo("Insertar al final  ·  O(n)")
        n = len(self.nodos)

        self.subtitulo("1. Recorremos la lista hasta el último nodo", espera=0.3)
        cursor = self.recorrer(
            n - 1, lambda nd, ultimo: "Su siguiente es NULL: es el último" if ultimo
            else "Su siguiente no es NULL: avanzamos")
        self.wait(0.5)
        self.limpiar_recorrido(cursor)

        self.subtitulo(f"2. Creamos el nodo nuevo ({valor}) y apuntamos su siguiente a NULL", espera=0.3)
        nuevo = self.crear_nodo(valor)
        nuevo.move_to([self.casilla_x(n, n + 1), ROW_Y - 1.9, 0])
        self.play(*self.acomodar(n + 1))
        self.play(FadeIn(nuevo, shift=UP * 0.3))
        nuevo.flecha_sal = self.flecha(nuevo[3].get_center(), self.destino_de(None))
        self.play(Create(nuevo.flecha_sal))
        self.vincular(nuevo)

        self.subtitulo("3. El antiguo último nodo apunta al nuevo", espera=0.3)
        self.re_enlazar(self.nodos[-1], nuevo)

        self.nodos.append(nuevo)
        self.play(*self.acomodar())
        self.wait(1)

    def buscar(self, valor):
        self.titulo("Buscar  ·  O(n)")
        idx = next(i for i, nd in enumerate(self.nodos) if nd.valor == valor)

        self.subtitulo(f"Buscamos el valor {valor} recorriendo desde la cabeza", espera=0.3)

        def mensaje(nd, ultimo):
            return f"¿{nd.valor} = {valor}?  " + (
                "¡Sí, lo encontramos!" if ultimo else "No, pasamos al siguiente")

        cursor = self.recorrer(idx, mensaje)
        self.play(self.nodos[idx][0].animate.set_fill(GREEN, opacity=0.6))
        self.subtitulo("En el peor caso recorremos toda la lista: O(n)", espera=1.5)
        self.limpiar_recorrido(cursor)

    def eliminar(self, valor):
        self.titulo("Eliminar un nodo  ·  O(n)")
        idx = next(i for i, nd in enumerate(self.nodos) if nd.valor == valor)
        anterior, objetivo = self.nodos[idx - 1], self.nodos[idx]

        self.subtitulo(f"1. Buscamos el nodo {valor} recordando el anterior", espera=0.3)
        cursor = self.recorrer(idx)
        self.play(Indicate(anterior, color=TEAL))
        self.limpiar_recorrido(cursor)

        self.subtitulo("2. Separamos el nodo que vamos a eliminar", espera=0.3)
        self.play(objetivo.animate.shift(DOWN * 1.8).set_color(RED))

        self.subtitulo("3. El anterior apunta al siguiente del nodo eliminado", espera=0.3)
        self.re_enlazar(anterior, objetivo.sig)

        self.subtitulo("4. Liberamos el nodo eliminado y cerramos el hueco", espera=0.3)
        objetivo.flecha_sal.clear_updaters()
        self.play(FadeOut(objetivo), FadeOut(objetivo.flecha_sal))
        self.nodos.remove(objetivo)
        self.play(*self.acomodar())
        self.wait(1)

    def complejidad(self):
        self.limpiar_escena()
        self.titulo("Complejidad de las operaciones")
        filas = [["Operación", "Tiempo"],
                 ["Insertar al inicio", "O(1)"],
                 ["Insertar al final (sin puntero a la cola)", "O(n)"],
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
