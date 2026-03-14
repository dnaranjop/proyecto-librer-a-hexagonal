from src.domain.repositories import CompraRepository

class MemoryCompraRepository(CompraRepository):
    def __init__(self):
        self.compras = []

    def formalizar_transaccion_compra(self, compra):
        self.compras.append(compra)
        print(f" [MEMORIA] Compra guardada para: {compra.usuario_nombre}")
        return compra

    def consultar_compras_del_cliente(self, nombre_cliente):
        return [c for c in self.compras if c.usuario_nombre == nombre_cliente]

    def recuperar_detalle_de_compra(self, compra_id):
        return next((c for c in self.compras if c.id == compra_id), None)

    def listar_historial_de_ventas(self):
        return self.compras

    def calcular_volumen_total_ingresos(self):
        return sum(c.total for c in self.compras)