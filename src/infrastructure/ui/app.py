import streamlit as st
import os
import sys

# Mantener la compatibilidad de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.application.ver_catalogo import VerCatalogo
from src.application.agregar_carrito import AgregarAlCarrito
from src.application.procesar_compra import ProcesarCompra
from src.infrastructure.persistence.sqlite_libro_repo import SQLiteLibroRepository
from src.infrastructure.persistence.sqlite_compra_repo import SQLiteCompraRepository
from src.infrastructure.notifications.console_notifier import ConsolePurchaseNotifier
from src.infrastructure.persistence.supabase_libro_repo import SupabaseLibroRepository
from src.infrastructure.persistence.supabase_compra_repo import SupabaseCompraRepository

# Credenciales de Supabase (Mantenidas según tu código)
SUPABASE_URL = "https://nywodndiaeqhtujovohf.supabase.co" 
SUPABASE_KEY = "sb_publishable_bpEYcnUwNJqRDWhJOTtPEw_GQ8trDgh"   

def run_ui():
    st.set_page_config(page_title="Mini-Librería Hexagonal", layout="wide", page_icon="📚")
    
    st.markdown("""
        <style>
        .main { background-color: #f5f7f9; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
        .libro-card { padding: 15px; border-radius: 10px; border: 1px solid #ddd; background: white; }
        </style>
    """, unsafe_allow_html=True)
    
    # --- INICIALIZACIÓN DE COMPONENTES ---
    # libro_repo = SQLiteLibroRepository() # Comentado según tu preferencia
    # compra_repo = SQLiteCompraRepository()
    
    # Inicializamos Supabase
    libro_repo = SupabaseLibroRepository(SUPABASE_URL, SUPABASE_KEY)
    compra_repo = SupabaseCompraRepository(SUPABASE_URL, SUPABASE_KEY)
    
    notifier = ConsolePurchaseNotifier()
    
    # Inyección de dependencias en los casos de uso
    cat_service = VerCatalogo(libro_repo)
    cart_service = AgregarAlCarrito(libro_repo)
    compra_service = ProcesarCompra(libro_repo, compra_repo)

    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    # --- SIDEBAR: CARRITO DE COMPRAS ---
    with st.sidebar:
        st.header("🛒 Tu Carrito")
        if not st.session_state.carrito:
            st.info("Aún no tienes productos.")
        else:
            total_compra = 0
            for i, item in enumerate(st.session_state.carrito):
                subtotal = item['precio'] * item['cantidad']
                total_compra += subtotal
                st.write(f"**{item['titulo']}**")
                st.caption(f"{item['cantidad']} x ${item['precio']/100:.2f} = ${subtotal/100:.2f}")
                st.divider()
            
            st.subheader(f"Total: ${total_compra/100:.2f}")
            
            nombre_cliente = st.text_input("Nombre del Cliente", key="cliente_nombre")
            
            if st.button("🚀 FINALIZAR COMPRA", type="primary"):
                if not nombre_cliente:
                    st.warning("⚠️ Ingresa el nombre del cliente.")
                else:
                    try:
                        # Orquestación del caso de uso
                        resultado = compra_service.ejecutar(nombre_cliente, st.session_state.carrito)
                        notifier.enviar_ticket(resultado)
                        st.success(f"✅ ¡Compra exitosa!")
                        st.session_state.carrito = []
                        st.balloons()
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ Error de Negocio: {e}")
                    except Exception as e:
                        st.error(f"🔥 Error inesperado: {e}")

    # --- CUERPO PRINCIPAL: CATÁLOGO ---
    st.title("📚 Librería Hexagonal")
    st.write("Bienvenido al catálogo gestionado con Arquitectura Limpia.")

    # IMPORTANTE: Aquí se usan los métodos actualizados del adaptador
    try:
        # Cambio: Aquí llamamos al servicio que usa el nuevo nombre del puerto
        libros_todos = cat_service.ejecutar() 
        
        categorias = sorted(list(set([l.categoria for l in libros_todos])))
        seleccion = st.multiselect("Filtrar por categoría:", categorias, default=categorias)

        st.divider()

        cols = st.columns(3)
        idx_col = 0

        for libro in libros_todos:
            if libro.categoria in seleccion:
                with cols[idx_col]:
                    with st.container():
                        st.markdown(f"### {libro.titulo}")
                        st.caption(f"🏷️ {libro.categoria} | ✍️ {libro.autor}")
                        st.write(f"**Precio:** ${libro.precio/100:.2f}")
                        st.write(f"**Stock disponible:** {libro.stock}")
                        
                        if st.button(f"➕ Agregar", key=f"btn_{libro.id}"):
                            # El cart_service también debe usar el nombre de puerto actualizado internamente
                            nuevo_cart, mensaje = cart_service.ejecutar(st.session_state.carrito, libro.id)
                            st.session_state.carrito = nuevo_cart
                            if "Error" in mensaje:
                                st.error(mensaje)
                            else:
                                st.toast(mensaje)
                                st.rerun()
                    st.write("") # Espaciador
                    
                idx_col = (idx_col + 1) % 3
    except Exception as e:
        st.error(f"Error al cargar el catálogo: {e}")

if __name__ == "__main__":
    run_ui()