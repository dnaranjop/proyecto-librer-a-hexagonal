import pytest
from datetime import datetime
from src.domain.libro import Libro
from src.domain.compra import Compra, ItemCompra

# === 1. PRUEBAS DE LA ENTIDAD LIBRO ===

def test_crear_libro_valido():
    libro = Libro(id=1, titulo="Clean Code", autor="Robert Martin", precio=4500, stock=10, categoria="Tecnología")
    assert libro.titulo == "Clean Code"
    assert libro.precio == 4500

def test_error_precio_negativo():
    with pytest.raises(ValueError):
        Libro(id=1, titulo="Libro Caro", autor="Autor", precio=-100, stock=10, categoria="X")

def test_error_titulo_corto():
    with pytest.raises(ValueError):
        Libro(id=1, titulo="A", autor="Autor", precio=1000, stock=10, categoria="X")

def test_verificar_stock_disponible():
    libro = Libro(id=1, titulo="Libro", autor="A", precio=100, stock=5, categoria="X")
    assert libro.tiene_stock(3) is True
    assert libro.tiene_stock(10) is False

def test_reducir_stock_exitoso():
    libro = Libro(id=1, titulo="Libro", autor="A", precio=100, stock=5, categoria="X")
    libro.reducir_stock(2)
    assert libro.stock == 3

def test_error_reducir_stock_insuficiente():
    libro = Libro(id=1, titulo="Libro", autor="A", precio=100, stock=2, categoria="X")
    with pytest.raises(ValueError, match="Stock insuficiente"):
        libro.reducir_stock(5)

# === 2. PRUEBAS DE LA ENTIDAD COMPRA ===

def test_crear_compra_valida():
    item = ItemCompra(libro_id=1, titulo="Libro A", cantidad=2, precio_unitario=1000)
    compra = Compra(usuario_nombre="Juan", items=[item], total=2000)
    assert compra.usuario_nombre == "Juan"
    assert len(compra.items) == 1

def test_error_compra_sin_items():
    with pytest.raises(ValueError):
        Compra(usuario_nombre="Juan", items=[], total=0)

def test_error_total_excede_limite():
    item = ItemCompra(libro_id=1, titulo="Libro Oro", cantidad=1, precio_unitario=2000000)
    with pytest.raises(ValueError, match="excede el límite"):
        Compra(usuario_nombre="Rico", items=[item], total=2000000)

def test_calcular_total_real():
    item1 = ItemCompra(libro_id=1, titulo="Libro 1", cantidad=1, precio_unitario=500)
    item2 = ItemCompra(libro_id=2, titulo="Libro 2", cantidad=2, precio_unitario=1000)
    compra = Compra(usuario_nombre="Pedro", items=[item1, item2], total=2500)
    assert compra.calcular_total_real() == 2500

def test_cambio_estado_a_completada():
    item = ItemCompra(libro_id=1, titulo="A", cantidad=1, precio_unitario=100)
    compra = Compra(usuario_nombre="X", items=[item], total=100)
    compra.completar()
    assert compra.estado == "Completada"

def test_error_cancelar_completada():
    item = ItemCompra(libro_id=1, titulo="A", cantidad=1, precio_unitario=100)
    compra = Compra(usuario_nombre="X", items=[item], total=100)
    compra.completar()
    with pytest.raises(ValueError, match="No se puede cancelar"):
        compra.cancelar()

# === 3. PRUEBAS DE INTEGRIDAD Y REGLAS ADICIONALES ===

def test_item_compra_subtotal():
    item = ItemCompra(libro_id=1, titulo="A", cantidad=3, precio_unitario=500)
    assert item.calcular_subtotal() == 1500

def test_compra_fecha_automatica():
    item = ItemCompra(libro_id=1, titulo="A", cantidad=1, precio_unitario=100)
    compra = Compra(usuario_nombre="X", items=[item], total=100)
    assert isinstance(compra.fecha, datetime)

def test_esta_disponible_libro():
    # Creamos un libro con stock 0
    libro = Libro(id=1, titulo="Libro Agotado", autor="Autor", precio=100, stock=0, categoria="C")
    # La prueba debe confirmar que NO está disponible
    assert libro.esta_disponible() is False
    # Si le sumamos stock, debe estar disponible
    libro.stock = 5
    assert libro.esta_disponible() is True

def test_validar_nombre_usuario_vacio():
    item = ItemCompra(libro_id=1, titulo="A", cantidad=1, precio_unitario=100)
    with pytest.raises(ValueError):
        Compra(usuario_nombre="", items=[item], total=100)

def test_item_cantidad_negativa_error():
    with pytest.raises(ValueError):
        ItemCompra(libro_id=1, titulo="A", cantidad=-1, precio_unitario=100)

def test_verificar_consistencia_total_falla():
    item = ItemCompra(libro_id=1, titulo="A", cantidad=1, precio_unitario=100)
    # Total enviado es 500 pero el item vale 100
    compra = Compra(usuario_nombre="X", items=[item], total=500)
    assert compra.verificar_consistencia_total() is False

def test_libro_id_opcional():
    libro = Libro(titulo="Libro Nuevo", autor="Autor", precio=100, stock=1, categoria="X")
    assert libro.id is None

def test_pydantic_validate_assignment():
    # Usamos un título válido de 2 caracteres o más ("AA")
    libro = Libro(titulo="AA", autor="B", precio=100, stock=10, categoria="C")
    
    # Probamos que si intentamos cambiar el stock a un número negativo después de creado
    # Pydantic debe lanzar un ValidationError
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        libro.stock = -1  # Esto dispara la validación de Pydantic

#python -m pytest tests/test_domain.py -v
#set PYTHONPATH=.