import sys
from pdf_parser import extraer_jugadores_pdf, extraer_info_partido
from buscar_coincidencias import buscar_coincidencias_en_todas_pestanas
from email_alertas import enviar_alerta_jugador

def procesar_acta_y_enviar_alertas(pdf_path, excel_path):
    """
    Proceso completo:
    1. Parsea el PDF
    2. Busca coincidencias en el Excel
    3. Envía alertas por email para jugadores destacados
    
    Args:
        pdf_path: ruta al PDF del acta
        excel_path: ruta al Excel con la base de datos de scouting
    """
    print("="*80)
    print("SISTEMA DE ALERTAS - AL NASSR FC")
    print("="*80)
    
    print("\n📄 PASO 1: Extrayendo información del PDF...")
    try:
        info_partido = extraer_info_partido(pdf_path)
        df_jugadores = extraer_jugadores_pdf(pdf_path)
        
        print(f"✅ Partido #{info_partido['ID_Partido']}")
        print(f"   Fecha: {info_partido['Fecha']} - {info_partido['Hora']}")
        print(f"   Estadio: {info_partido['Estadio']}")
        print(f"   Total jugadores convocados: {len(df_jugadores)}")
        
    except Exception as e:
        print(f"❌ Error al procesar PDF: {e}")
        return
    
    print("\n🔍 PASO 2: Buscando coincidencias en base de datos...")
    try:
        jugadores_encontrados = buscar_coincidencias_en_todas_pestanas(df_jugadores, excel_path)
        
        print(f"✅ Jugadores encontrados en base de datos: {len(jugadores_encontrados)}")
        
        if len(jugadores_encontrados) == 0:
            print("\n⚠️  No se encontraron jugadores destacados en esta convocatoria")
            return
        
        print("\nJugadores destacados encontrados:")
        for j in jugadores_encontrados:
            print(f"  • {j['Nombre']} (#{j['Dorsal']}) - {j['Equipo']}")
            print(f"    Decisión: {j['Decisión']} | Performance: {j['Performance']}")
        
    except Exception as e:
        print(f"❌ Error al buscar coincidencias: {e}")
        return
    
    print("\n📧 PASO 3: Enviando alertas por email...")
    alertas_enviadas = 0
    
    for jugador in jugadores_encontrados:
        jugador_info = {
            'Nombre': jugador['Nombre'],
            'Equipo': jugador['Equipo'],
            'Dorsal': jugador['Dorsal'],
            'Decisión': jugador['Decisión'],
            'Posicion': jugador['Posicion'],
            'Tipo': jugador['Tipo'],
            'Performance': jugador['Performance'],
            'Watch': jugador['Watch'],
            'Scout': jugador['Scout'],
            'Año_Nacimiento': jugador['Año_Nacimiento'],
            'Partido': f"#{info_partido['ID_Partido']} - {info_partido['Fecha']}"
        }
        
        if enviar_alerta_jugador(jugador_info):
            alertas_enviadas += 1
    
    print(f"\n✅ Proceso completado: {alertas_enviadas}/{len(jugadores_encontrados)} alertas enviadas")
    print("="*80)
    
    return jugadores_encontrados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 sistema_alertas_completo.py <ruta_al_pdf>")
        print("\nEjemplo:")
        print("  python3 sistema_alertas_completo.py /ruta/al/Acta2AlNassr.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    excel_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/mreportsyouth.xlsx'
    
    procesar_acta_y_enviar_alertas(pdf_path, excel_path)
