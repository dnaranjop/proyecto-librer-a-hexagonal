import streamlit as st
import sqlite3
import datetime

# VIOLACIÓN 1: Conexión directa a un archivo físico desde la interfaz
# Si el archivo no existe o cambia de ruta, la UI se rompe.
DB_NAME = "libreria_monolitica.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Creación de tablas mezclada con la lógica de arranque
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros 
                      (id INTEGER PRIMARY KEY, titulo TEXT, stock INTEGER, precio INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS compras 
                      (id INTEGER PRIMARY KEY, usuario TEXT, total INTEGER, fecha TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.title("📚 Librería Monolítica (Legacy)")
st.warning("⚠️ Este código mezcla UI, Base de Datos y Negocio.")

def comprar_libro():
    st.header("Procesar Compra Directa")
    libro_id = st.number_input("ID del Libro", min_value=1)
    cantidad = st.number_input("Cantidad a comprar", min_value=1)
    usuario = st.text_input("Nombre del Cliente")

    if st.button("Finalizar Compra"):
        # VIOLACIÓN 2: Uso de SQL crudo (Raw SQL) dentro de la capa de presentación
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Consulta directa
        cursor.execute("SELECT titulo, stock, precio FROM libros WHERE id = ?", (libro_id,))
        libro = cursor.fetchone()

        if libro:
            titulo, stock_actual, precio = libro
            
            # VIOLACIÓN 3: La lógica de negocio (validar stock) vive en un IF de la UI
            if stock_actual >= cantidad:
                nuevo_stock = stock_actual - cantidad
                
                # Actualización directa del stock
                cursor.execute("UPDATE libros SET stock = ? WHERE id = ?", (nuevo_stock, libro_id))
                
                # Registro de la compra
                total = precio * cantidad
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cursor.execute("INSERT INTO compras (usuario, total, fecha) VALUES (?, ?, ?)",
                               (usuario, total, fecha))
                
                conn.commit()
                st.success(f"✅ ¡Vendido! {titulo} por ${total/100:.2f}")
            else:
                st.error(f"❌ Solo quedan {stock_actual} unidades.")
        else:
            st.error("❌ El libro no existe en la base de datos.")
        
        conn.close()

comprar_libro()