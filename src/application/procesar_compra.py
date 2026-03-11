from src.domain.compra import Compra, ItemCompra
from src.domain.repositories import LibroRepository, CompraRepository

class ProcesarCompra:
    def __init__(self, libro_repo: LibroRepository, compra_repo: CompraRepository):
        self.libro_repo = libro_repo
        self.compra_repo = compra_repo

    def ejecutar(self, usuario_nombre: str, carrito: list):
        items_dominio = []
        
        for item in carrito:
            libro = self.libro_repo.obtener_por_id(item['id'])
            if libro and libro.tiene_stock(item['cantidad']):
                # Lógica de dominio: reducir stock
                libro.reducir_stock(item['cantidad'])
                self.libro_repo.actualizar_stock(libro.id, libro.stock)
                
                # Crear item de compra
                items_dominio.append(ItemCompra(
                    libro_id=libro.id,
                    titulo=libro.titulo,
                    cantidad=item['cantidad'],
                    precio_unitario=libro.precio
                ))

        nueva_compra = Compra(
            id=None,
            usuario_nombre=usuario_nombre,
            items=items_dominio,
            total=sum(i.calcular_subtotal() for i in items_dominio)
        )
        
        return self.compra_repo.guardar(nueva_compra)