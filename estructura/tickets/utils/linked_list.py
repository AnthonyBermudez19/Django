class Nodo:
    def __init__(self, valor):
        self.valor = valor  # El valor almacenado en el nodo.
        self.siguiente = None  # Apuntador al siguiente nodo (inicialmente None).


class ColaConListaEnlazada:
    def __init__(self):
        self.cabeza=None

    def agregar(self, elemento):
        nuevo_nodo = Nodo(elemento)  # Crear un nuevo nodo con el valor proporcionado.
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual=self.cabeza
            while actual.siguiente:
                actual=actual.siguiente
            actual.siguiente=nuevo_nodo

    def lista(self):
        actual=self.cabeza
        while actual:
            yield actual.valor
            actual=actual.siguiente

    def tomar_primero(self):
        if self.cabeza is None:
            raise IndexError("La cola está vacía")  # Si la cola está vacía, no se puede tomar un ticket

        primer_ticket = self.cabeza.valor  # Obtener el valor del primer nodo
        self.cabeza = self.cabeza.siguiente  # Mover la cabeza al siguiente nodo

        return primer_ticket