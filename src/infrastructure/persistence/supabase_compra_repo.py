from supabase import create_client, Client
from src.domain.repositories import CompraRepository

class SupabaseCompraRepository(CompraRepository):
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    # CAMBIO: guardar -> formalizar_transaccion_compra
    def formalizar_transaccion_compra(self, compra):
        # 1. Preparar la fecha como texto
        fecha_texto = compra.fecha.isoformat() if hasattr(compra.fecha, 'isoformat') else str(compra.fecha)

        # 2. Insertar la compra (Maestro)
        compra_dict = {
            "usuario_nombre": compra.usuario_nombre,
            "total": compra.total,
            "fecha": fecha_texto
        }
        
        res_compra = self.supabase.table("compras").insert(compra_dict).execute()
        
        # 3. Obtener el ID generado
        compra_id = res_compra.data[0]['id']
        compra.id = compra_id

        # 4. Preparar y guardar los items (Detalle)
        items_para_insertar = []
        for item in compra.items:
            items_para_insertar.append({
                "compra_id": compra_id,
                "libro_id": item.libro_id,
                "titulo": item.titulo,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario
            })
        
        if items_para_insertar:
            self.supabase.table("items_compra").insert(items_para_insertar).execute()
        
        return compra

    # CAMBIO: obtener_por_id -> recuperar_detalle_de_compra
    def recuperar_detalle_de_compra(self, compra_id):
        response = self.supabase.table("compras").select("*").eq("id", compra_id).execute()
        return response.data[0] if response.data else None

    # CAMBIO: obtener_todas -> listar_historial_de_ventas
    def listar_historial_de_ventas(self):
        response = self.supabase.table("compras").select("*").execute()
        return response.data

    # CAMBIO: obtener_por_usuario -> consultar_compras_del_cliente
    def consultar_compras_del_cliente(self, nombre_usuario):
        response = self.supabase.table("compras").select("*").eq("usuario_nombre", nombre_usuario).execute()
        return response.data

    # CAMBIO: contar_total_ventas -> calcular_volumen_total_ingresos
    def calcular_volumen_total_ingresos(self):
        response = self.supabase.table("compras").select("total").execute()
        return sum(item['total'] for item in response.data) if response.data else 0