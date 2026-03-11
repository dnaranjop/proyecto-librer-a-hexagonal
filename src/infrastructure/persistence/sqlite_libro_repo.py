import sqlite3
from src.domain.libro import Libro
from src.domain.repositories import LibroRepository

class SQLiteLibroRepository(LibroRepository):
    def __init__(self, db_path="libreria.db"):
        self.db_path = db_path

    def obtener_todos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, titulo, autor, precio, stock, categoria FROM libros")
            return [Libro(*row) for row in cursor.fetchall()]

    def obtener_por_id(self, libro_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, titulo, autor, precio, stock, categoria FROM libros WHERE id=?", (libro_id,))
            row = cursor.fetchone()
            return Libro(*row) if row else None

    def actualizar_stock(self, libro_id, nuevo_stock):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE libros SET stock=? WHERE id=?", (nuevo_stock, libro_id))
            conn.commit()

    # --- MÉTODOS QUE FALTABAN ---
    
    def guardar(self, libro: Libro) -> Libro:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if libro.id:
                cursor.execute("""
                    UPDATE libros SET titulo=?, autor=?, precio=?, stock=?, categoria=? WHERE id=?
                """, (libro.titulo, libro.autor, libro.precio, libro.stock, libro.categoria, libro.id))
            else:
                cursor.execute("""
                    INSERT INTO libros (titulo, autor, precio, stock, categoria) VALUES (?, ?, ?, ?, ?)
                """, (libro.titulo, libro.autor, libro.precio, libro.stock, libro.categoria))
                libro.id = cursor.lastrowid
            conn.commit()
            return libro

    def obtener_por_categoria(self, categoria: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, titulo, autor, precio, stock, categoria FROM libros WHERE categoria=?", (categoria,))
            return [Libro(*row) for row in cursor.fetchall()]