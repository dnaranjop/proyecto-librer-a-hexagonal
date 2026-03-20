from src.domain.repositories import LibroRepository
from src.domain.libro import Libro

class MemoryLibroRepository(LibroRepository):
    def __init__(self):
        # Datos simulados
        self.libros = [
            Libro(id=1, titulo="Cien Años de Soledad", autor="Gabo", precio=50000, stock=10, categoria="Ficción"),
            Libro(id=2, titulo="Clean Architecture", autor="Uncle Bob", precio=120000, stock=5, categoria="Tecnología"),
            Libro(id=3, titulo="Don Quijote", autor="Cervantes", precio=45000, stock=0, categoria="Clásico")
        ]

    def consultar_catalogo_completo(self):
        return self.libros

    def buscar_libro_por_identificador(self, libro_id):
        return next((l for l in self.libros if l.id == libro_id), None)

    def sincronizar_disponibilidad_stock(self, libro_id, nueva_cantidad):
        for libro in self.libros:
            if libro.id == libro_id:
                libro.stock = nueva_cantidad
                return True
        return False

    def filtrar_libros_por_categoria(self, categoria):
        return [l for l in self.libros if l.categoria == categoria]

    def registrar_nuevo_libro(self, libro):
        self.libros.append(libro)
        return libro