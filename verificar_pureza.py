import os
import sys

def verificar_pureza_arquitectonica():
    # La carpeta que debe ser pura
    ruta_dominio = os.path.join("src", "domain")
    
    # Librerías y términos prohibidos en la capa de Dominio
    terminos_prohibidos = [
        'supabase', 'streamlit', 'sqlite3', 'infrastructure', 
        'requests', 'pandas', 'application', 'ui', 'persistence'
    ]
    
    violaciones = 0
    archivos_analizados = 0

    print("\n" + "="*60)
    print("🔍 VERIFICADOR DE PUREZA ARQUITECTÓNICA - FASE 2")
    print("="*60)
    
    if not os.path.exists(ruta_dominio):
        print(f"❌ ERROR: No se encontró la carpeta {ruta_dominio}")
        return 1

    for raiz, dirs, archivos in os.walk(ruta_dominio):
        for archivo in archivos:
            if archivo.endswith(".py") and archivo != "__init__.py":
                archivos_analizados += 1
                ruta_completa = os.path.join(raiz, archivo)
                
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                    for num_linea, contenido in enumerate(lineas, 1):
                        linea_limpia = contenido.lower().strip()
                        # Solo analizar líneas que tengan imports
                        if "import" in linea_limpia or "from" in linea_limpia:
                            for termino in terminos_prohibidos:
                                if termino in linea_limpia:
                                    print(f"❌ VIOLACIÓN DETECTADA")
                                    print(f"   Archivo: {ruta_completa}")
                                    print(f"   Línea {num_linea}: {contenido.strip()}")
                                    print(f"   Motivo: El Dominio no debe conocer '{termino}'\n")
                                    violaciones += 1
    
    print("-" * 60)
    print(f"📊 RESUMEN DEL ANÁLISIS:")
    print(f"   Archivos analizados: {archivos_analizados}")
    print(f"   Violaciones encontradas: {violaciones}")
    print("-" * 60)

    if violaciones == 0:
        print("✅ RESULTADO: PUREZA TOTAL. El dominio cumple con la Fase 2.")
        return 0
    else:
        print("⚠️ RESULTADO: El dominio está contaminado. Debes limpiar los imports.")
        return 1

if __name__ == "__main__":
    sys.exit(verificar_pureza_arquitectonica())

# python verificar_pureza.py