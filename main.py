import os
import sqlite3
import subprocess
import sys

def init_db():
    """Crea la base de datos y tablas si no existen"""
    conn = sqlite3.connect("libreria.db")
    cursor = conn.cursor()
    
    # Tabla de Libros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            precio INTEGER,
            stock INTEGER,
            categoria TEXT
        )
    """)
    
    # Insertar datos de prueba si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM libros")
    if cursor.fetchone()[0] == 0:
        libros_iniciales = [
    ('El Quijote', 'Miguel de Cervantes', 2000, 10, 'Clásicos'),
    ('Clean Code', 'Robert Martin', 4500, 5, 'Tecnología'),
    ('Cien Años de Soledad', 'Gabriel García Márquez', 3500, 8, 'Ficción'),
    ('El Principito', 'Antoine de Saint-Exupéry', 1500, 15, 'Infantil'),
    ('Design Patterns', 'Erich Gamma', 5500, 4, 'Tecnología'),
    ('1984', 'George Orwell', 28000, 12, 'Distopía'),
    ('Crónica de una muerte anunciada', 'G. García Márquez', 2200, 6, 'Ficción'),
    ('Refactoring', 'Martin Fowler', 4800, 3, 'Tecnología')
]
        
        cursor.executemany("INSERT INTO libros (titulo, autor, precio, stock, categoria) VALUES (?, ?, ?, ?, ?)", libros_iniciales)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos lista. Iniciando Streamlit...")
    
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/infrastructure/ui/app.py"])