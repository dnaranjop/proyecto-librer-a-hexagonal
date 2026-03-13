"""
Caso de Uso: ProcesarCompra
Capa de Aplicación - Orquestador del flujo de negocio.
"""
from src.domain.compra import Compra, ItemCompra
from src.domain.repositories import LibroRepository, CompraRepository

class ProcesarCompra:
    def __init__(self, libro_repo: LibroRepository, compra_repo: CompraRepository):
        self.libro_repo = libro_repo
        self.compra_repo = compra_repo

    def ejecutar(self, usuario_nombre: str, carrito: list) -> Compra:
        """
        Orquesta el proceso de compra asegurando la integridad del negocio.
        """
        items_para_compra = []
        libros_a_actualizar = []

        # 1. Validación y Preparación
        for item in carrito:
            libro_id = item.get('id')
            cantidad = item.get('cantidad')

            # CAMBIO: obtener_por_id -> buscar_libro_por_identificador
            libro = self.libro_repo.buscar_libro_por_identificador(libro_id)
            
            if not libro:
                raise ValueError(f"El libro con ID {libro_id} no existe.")

            # 2. Delegar lógica al DOMINIO
            libro.reducir_stock(cantidad) 
            
            libros_a_actualizar.append(libro)

            # 3. Crear objetos de valor
            items_para_compra.append(ItemCompra(
                libro_id=libro.id,
                titulo=libro.titulo,
                cantidad=cantidad,
                precio_unitario=libro.precio
            ))

        # 4. Crear el Agregado Compra
        nueva_compra = Compra(
            usuario_nombre=usuario_nombre,
            items=items_para_compra,
            total=sum(i.calcular_subtotal() for i in items_para_compra)
        )

        # 5. Persistencia (Infraestructura)
        for libro_modificado in libros_a_actualizar:
            # CAMBIO: actualizar_stock -> sincronizar_disponibilidad_stock
            self.libro_repo.sincronizar_disponibilidad_stock(libro_modificado.id, libro_modificado.stock)

        resultado = self.compra_repo.formalizar_transaccion_compra(nueva_compra)
        return resultado