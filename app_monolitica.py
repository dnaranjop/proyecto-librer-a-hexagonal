import streamlit as st
from supabase import create_client
import datetime

# VIOLACIÓN 1: Credenciales y conexión directa en la UI
url = "https://tu-proyecto.supabase.co"
key = "tu-key-secreta"
supabase = create_client(url, key)

st.title("Librería Monolítica")

# VIOLACIÓN 2: Lógica de negocio mezclada con la base de datos
def comprar_libro():
    st.header("Realizar Compra")
    libro_id = st.number_input("ID del Libro", min_value=1)
    cantidad = st.number_input("Cantidad", min_value=1)
    usuario = st.text_input("Tu Nombre")

    if st.button("Finalizar Compra"):
        # VIOLACIÓN 3: No hay validación de dominio (Pydantic), se confía en el input
        # Consulta directa a la base de datos desde la UI
        res = supabase.table("libros").select("*").eq("id", libro_id).execute()
        
        if res.data:
            libro = res.data[0]
            if libro['stock'] >= cantidad:
                nuevo_stock = libro['stock'] - cantidad
                # Actualización directa
                supabase.table("libros").update({"stock": nuevo_stock}).eq("id", libro_id).execute()
                
                # Registro de compra directo
                total = libro['precio'] * cantidad
                supabase.table("compras").insert({
                    "usuario": usuario,
                    "total": total,
                    "fecha": str(datetime.datetime.now())
                }).execute()
                st.success(f"¡Compra exitosa! Total: ${total/100}")
            else:
                st.error("No hay stock suficiente")

comprar_libro()