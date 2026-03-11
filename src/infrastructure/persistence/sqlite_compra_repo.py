import sqlite3
from src.domain.compra import Compra
from src.domain.repositories import CompraRepository

class SQLiteCompraRepository(CompraRepository):
    def __init__(self, db_path="libreria.db"):
        self.db_path = db_path
        self._crear_tablas()

    def _crear_tablas(self):
        with sqlite3.connect(self.db_path) as conn:
            # Tabla Maestra de Compras
            conn.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_nombre TEXT,
                    total INTEGER,
                    estado TEXT,
                    fecha TEXT
                )
            """)
            # Tabla Detalle de Items
            conn.execute("""
                CREATE TABLE IF NOT EXISTS items_compra (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    compra_id INTEGER,
                    libro_id INTEGER,
                    titulo TEXT,
                    cantidad INTEGER,
                    precio_unitario INTEGER,
                    FOREIGN KEY(compra_id) REFERENCES compras(id)
                )
            """)

    def guardar(self, compra: Compra) -> Compra:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 1. Insertar la cabecera de la compra
            cursor.execute("""
                INSERT INTO compras (usuario_nombre, total, estado, fecha)
                VALUES (?, ?, ?, ?)
            """, (compra.usuario_nombre, compra.total, compra.estado, compra.fecha.isoformat()))
            
            compra.id = cursor.lastrowid
            
            # 2. Insertar cada item del detalle
            for item in compra.items:
                cursor.execute("""
                    INSERT INTO items_compra (compra_id, libro_id, titulo, cantidad, precio_unitario)
                    VALUES (?, ?, ?, ?, ?)
                """, (compra.id, item.libro_id, item.titulo, item.cantidad, item.precio_unitario))
            
            conn.commit()
            return compra

    # Los demás métodos pueden quedar como 'pass' por ahora si no los usas en la UI
    def obtener_por_id(self, id): pass
    def obtener_todas(self, limite=50): pass
    def obtener_por_usuario(self, nombre): pass
    def contar_total_ventas(self): pass