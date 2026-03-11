from src.domain.repositories import LibroRepository

class AgregarAlCarrito:
    def __init__(self, libro_repo: LibroRepository):
        self.libro_repo = libro_repo

    def ejecutar(self, carrito_actual: list, libro_id: int):
        """
        Valida si hay stock antes de permitir agregar al carrito.
        """
        libro = self.libro_repo.obtener_por_id(libro_id)
        
        if not libro:
            return carrito_actual, "Error: El libro no existe."
            
        if not libro.tiene_stock(1):
            return carrito_actual, f"Error: No hay stock de '{libro.titulo}'."

        # Si ya está en el carrito, aumentamos cantidad (opcional)
        for item in carrito_actual:
            if item['id'] == libro_id:
                item['cantidad'] += 1
                return carrito_actual, f"Se aumentó la cantidad de {libro.titulo}."

        # Si es nuevo, lo agregamos
        nuevo_item = {
            'id': libro.id,
            'titulo': libro.titulo,
            'precio': libro.precio,
            'cantidad': 1
        }
        carrito_actual.append(nuevo_item)
        return carrito_actual, f"{libro.titulo} añadido al carrito."