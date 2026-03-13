"""
Entidad del Dominio: Libro
Lógica de negocio pura, utilizando Pydantic para validación de invariantes.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Libro(BaseModel):
    """
    Entidad Libro - Representa un libro en el dominio del negocio.
    Cumple con la Fase 2: Validación de invariantes con Pydantic.
    """
    
    id: Optional[int] = None
    titulo: str = Field(..., min_length=2, description="El título debe tener al menos 2 caracteres")
    autor: str = Field(..., min_length=1, description="El autor es obligatorio")
    precio: int = Field(..., gt=0, description="El precio debe ser un valor positivo")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    categoria: str

    # --- Validaciones de Invariantes (Reglas de Negocio) ---
    
    field_validator('titulo')
    def titulo_no_vacio(cls, v):
        if not v.strip():
            raise ValueError("El título no puede consistir solo en espacios en blanco")
        return v

    # --- Métodos de Comportamiento (Lógica de Negocio) ---

    def tiene_stock(self, cantidad: int = 1) -> bool:
        """Regla de negocio: Verificar disponibilidad"""
        return self.stock >= cantidad
    
    def reducir_stock(self, cantidad: int) -> None:
        """
        Regla de negocio: Reducir stock después de una venta.
        Lanza ValueError si no hay stock suficiente.
        """
        if not self.tiene_stock(cantidad):
            raise ValueError(
                f"Stock insuficiente. Disponible: {self.stock}, Solicitado: {cantidad}"
            )
        self.stock -= cantidad
    
    def calcular_subtotal(self, cantidad: int) -> int:
        """Regla de negocio: Calcular precio total en centavos"""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return self.precio * cantidad
    
    def esta_disponible(self) -> bool:
        """Verificar si el libro está disponible para venta"""
        return self.stock > 0

    class Config:
        """Configuración de Pydantic"""
        validate_assignment = True  # Valida reglas incluso si cambias un valor después de crear el objeto