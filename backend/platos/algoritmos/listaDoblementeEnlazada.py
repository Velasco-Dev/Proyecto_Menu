class Nodo:
    def __init__(self, plato, puntuacion_total):
        self.plato = plato
        self.puntuacion_total = puntuacion_total
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamanio = 0

    def insertar_ordenado(self, plato, puntuacion_total):
        nuevo = Nodo(plato, puntuacion_total)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            actual = self.cabeza
            while actual and actual.puntuacion_total >= puntuacion_total:
                anterior = actual
                actual = actual.siguiente
            if actual == self.cabeza:
                # Insertar al inicio
                nuevo.siguiente = self.cabeza
                self.cabeza.anterior = nuevo
                self.cabeza = nuevo
            elif actual is None:
                # Insertar al final
                nuevo.anterior = self.cola
                self.cola.siguiente = nuevo
                self.cola = nuevo
            else:
                # Insertar en medio
                nuevo.siguiente = actual
                nuevo.anterior = actual.anterior
                actual.anterior.siguiente = nuevo
                actual.anterior = nuevo
        self.tamanio += 1

    def recorrerAdelante(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(f'{actual.plato["nombre"]} (Puntuación: {actual.puntuacion_total})')
            actual = actual.siguiente
            print("Recorriendo adelante:", " <--> ".join(elementos))
        return " <--> ".join(elementos) 

lista = ListaDoblementeEnlazada()
