"""
Entidad del Dominio: Compra
Representa una compra utilizando Pydantic para validación de reglas de negocio.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class ItemCompra(BaseModel):
    """
    Objeto de Valor: Representa un item dentro de una compra.
    """
    libro_id: int
    titulo: str = Field(..., min_length=1)
    cantidad: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")
    precio_unitario: int = Field(..., ge=0)
    
    def calcular_subtotal(self) -> int:
        """Calcular subtotal del item"""
        return self.precio_unitario * self.cantidad

class Compra(BaseModel):
    """
    Agregado Raíz: Representa una compra completa.
    Cumple con los requisitos de validación de invariantes de la Fase 2.
    """
    
    id: Optional[int] = None
    usuario_nombre: str = Field(..., min_length=1, description="El nombre de usuario es obligatorio")
    items: List[ItemCompra] = Field(..., min_items=1, description="La compra debe tener al menos un item")
    total: int = Field(..., ge=0)
    estado: str = "Pendiente"  # Pendiente, Completada, Cancelada
    fecha: datetime = Field(default_factory=datetime.now)

    # --- Validaciones de Invariantes ---

    field_validator('total')
    def validar_limite_maximo(cls, v):
        LIMITE_MAXIMO = 1000000 
        if v > LIMITE_MAXIMO:
            raise ValueError(f"La compra excede el límite permitido de ${LIMITE_MAXIMO/100:.2f}")
        return v

    field_validator('items')
    def validar_lista_no_vacia(cls, v):
        if len(v) == 0:
            raise ValueError("La lista de productos no puede estar vacía")
        return v

    # --- Métodos de Comportamiento (Lógica de Negocio) ---
    
    def calcular_total_real(self) -> int:
        """Calcula el total basado en la suma de sus items"""
        return sum(item.calcular_subtotal() for item in self.items)
    
    def verificar_consistencia_total(self) -> bool:
        """Verifica que el total informado coincida con la suma de los items"""
        return self.total == self.calcular_total_real()
    
    def completar(self) -> None:
        """Regla de negocio: Finalizar proceso de compra"""
        if self.estado == "Completada":
            raise ValueError("La compra ya está completada")
        if self.estado == "Cancelada":
            raise ValueError("No se puede completar una compra cancelada")
        self.estado = "Completada"
    
    def cancelar(self) -> None:
        """Regla de negocio: Anular compra"""
        if self.estado == "Completada":
            raise ValueError("No se puede cancelar una compra ya completada")
        self.estado = "Cancelada"

    class Config:
        validate_assignment = True # Asegura que si cambias el estado manualmente, se validen las reglas