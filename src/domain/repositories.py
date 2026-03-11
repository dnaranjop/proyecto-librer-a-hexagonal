"""
Repositorios (Puertos de Salida) - Interfaces del Dominio
Fase 2: Definición de contratos por intención de negocio.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .libro import Libro
from .compra import Compra

class LibroRepository(ABC):
    """
    Puerto de Salida para la gestión del catálogo.
    Define QUÉ necesita el negocio del inventario.
    """
    
    @abstractmethod
    def consultar_catalogo_completo(self) -> List[Libro]:
        """Intención: Mostrar al cliente todos los libros disponibles."""
        pass
    
    @abstractmethod
    def buscar_libro_por_identificador(self, libro_id: int) -> Optional[Libro]:
        """Intención: Validar existencia de un libro antes de procesar."""
        pass
    
    @abstractmethod
    def filtrar_libros_por_categoria(self, categoria: str) -> List[Libro]:
        """Intención: Segmentar la oferta comercial."""
        pass
    
    @abstractmethod
    def registrar_nuevo_libro(self, libro: Libro) -> Libro:
        """Intención: Expandir el catálogo de la librería."""
        pass
    
    @abstractmethod
    def sincronizar_disponibilidad_stock(self, libro_id: int, nuevo_stock: int) -> None:
        """Intención: Asegurar que el stock físico coincida con el sistema."""
        pass


class CompraRepository(ABC):
    """
    Puerto de Salida para el registro de la actividad comercial.
    """
    
    @abstractmethod
    def formalizar_transaccion_compra(self, compra: Compra) -> Compra:
        """Intención: Dejar registro legal y contable de la venta."""
        pass
    
    @abstractmethod
    def recuperar_detalle_de_compra(self, compra_id: int) -> Optional[Compra]:
        """Intención: Consultar una venta para soporte o reclamos."""
        pass
    
    @abstractmethod
    def listar_historial_de_ventas(self, limite: int = 50) -> List[Compra]:
        """Intención: Auditoría de movimientos recientes."""
        pass
    
    @abstractmethod
    def consultar_compras_del_cliente(self, usuario_nombre: str) -> List[Compra]:
        """Intención: Fidelización y seguimiento del cliente."""
        pass
    
    @abstractmethod
    def calcular_volumen_total_ingresos(self) -> int:
        """Intención: Reporte de éxito financiero (en centavos)."""
        pass