# Este es un nuevo Adaptador de Salida
class ConsolePurchaseNotifier:
    def enviar_ticket(self, compra):
        print("\n" + "="*30)
        print("🎫 TICKET DE VENTA GENERADO")
        print(f"Cliente: {compra.usuario_nombre}")
        print(f"Total: ${compra.total / 100:.2f}")
        print(f"Fecha: {compra.fecha}")
        print("="*30 + "\n")