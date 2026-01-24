"""
Script de diagnóstico para verificar por qué los jugadores no se están encontrando
"""
import pandas as pd
from google_sheets import leer_todas_las_pestanas
from buscar_coincidencias import normalizar_nombre, normalizar_equipo, similitud_nombres

def diagnosticar_jugador(nombre, dorsal, equipo):
    """
    Diagnostica por qué un jugador específico no se está encontrando
    """
    print(f"\n{'='*80}")
    print(f"🔍 DIAGNÓSTICO PARA: {nombre} (#{dorsal}) - {equipo}")
    print(f"{'='*80}")
    
    # Normalizar datos de entrada
    nombre_norm = normalizar_nombre(nombre)
    equipo_norm = normalizar_equipo(equipo)
    
    print(f"\n📝 Datos normalizados:")
    print(f"   Nombre: '{nombre}' → '{nombre_norm}'")
    print(f"   Equipo: '{equipo}' → '{equipo_norm}'")
    print(f"   Dorsal: {dorsal}")
    
    # Leer todas las pestañas
    print(f"\n📊 Leyendo Google Sheets...")
    sheets_dict = leer_todas_las_pestanas()
    print(f"   ✅ {len(sheets_dict)} pestañas cargadas")
    
    mejores_coincidencias = []
    
    # Buscar en todas las pestañas
    for sheet_name, df_sheet in sheets_dict.items():
        if 'Name' not in df_sheet.columns or 'Number' not in df_sheet.columns:
            continue
        
        print(f"\n🔎 Buscando en pestaña: {sheet_name}")
        print(f"   Total jugadores en pestaña: {len(df_sheet)}")
        
        for idx, row in df_sheet.iterrows():
            nombre_excel = normalizar_nombre(row.get('Name', ''))
            dorsal_excel = row.get('Number', None)
            equipo_excel = normalizar_equipo(row.get('Team', ''))
            
            # Calcular coincidencias
            coincide_dorsal = False
            if pd.notna(dorsal_excel):
                try:
                    coincide_dorsal = int(dorsal_excel) == int(dorsal)
                except:
                    pass
            
            coincide_equipo = equipo_norm in equipo_excel or equipo_excel in equipo_norm
            similitud = similitud_nombres(nombre_norm, nombre_excel)
            
            # Si hay alguna similitud interesante, guardarla
            if similitud > 0.5 or coincide_dorsal:
                mejores_coincidencias.append({
                    'pestaña': sheet_name,
                    'nombre_excel': row.get('Name', ''),
                    'nombre_norm': nombre_excel,
                    'dorsal_excel': dorsal_excel,
                    'equipo_excel': row.get('Team', ''),
                    'equipo_norm': equipo_excel,
                    'similitud': similitud,
                    'coincide_dorsal': coincide_dorsal,
                    'coincide_equipo': coincide_equipo,
                    'decision': row.get('Profile Decision', 'N/A'),
                    'performance': row.get('Performance', 'N/A')
                })
    
    # Ordenar por similitud
    mejores_coincidencias.sort(key=lambda x: x['similitud'], reverse=True)
    
    print(f"\n📋 MEJORES COINCIDENCIAS ENCONTRADAS (Top 10):")
    print(f"{'─'*80}")
    
    if not mejores_coincidencias:
        print("   ❌ No se encontraron coincidencias")
    else:
        for i, match in enumerate(mejores_coincidencias[:10], 1):
            print(f"\n   {i}. {match['nombre_excel']} (#{match['dorsal_excel']}) - {match['equipo_excel']}")
            print(f"      Pestaña: {match['pestaña']}")
            print(f"      Similitud nombre: {match['similitud']:.2%}")
            print(f"      Coincide dorsal: {'✅' if match['coincide_dorsal'] else '❌'}")
            print(f"      Coincide equipo: {'✅' if match['coincide_equipo'] else '❌'}")
            print(f"      Decisión: {match['decision']}")
            
            # Verificar si cumpliría los criterios actuales
            cumple_criterio_1 = match['coincide_dorsal'] and match['coincide_equipo'] and match['similitud'] > 0.7
            cumple_criterio_2 = match['similitud'] > 0.85 and match['coincide_equipo']
            
            if cumple_criterio_1 or cumple_criterio_2:
                print(f"      🎯 SERÍA DETECTADO (cumple criterios)")
            else:
                print(f"      ⚠️  NO SERÍA DETECTADO")
                if not match['coincide_dorsal']:
                    print(f"         - Dorsal no coincide: {dorsal} vs {match['dorsal_excel']}")
                if not match['coincide_equipo']:
                    print(f"         - Equipo no coincide: '{equipo_norm}' vs '{match['equipo_norm']}'")
                if match['similitud'] <= 0.7:
                    print(f"         - Similitud baja: {match['similitud']:.2%} (necesita >70% o >85%)")
    
    print(f"\n{'='*80}\n")


def diagnosticar_partido(match_id):
    """
    Diagnostica todos los jugadores de un partido específico
    """
    from saff_api import get_event_details, process_lineups
    
    print(f"\n🏟️  DIAGNÓSTICO DE PARTIDO: {match_id}")
    print(f"{'='*80}")
    
    # Obtener detalles del partido
    event_data = get_event_details(match_id)
    
    if not event_data:
        print("❌ No se pudo obtener información del partido")
        return
    
    home_team = event_data.get('homeTeam', {}).get('name', 'Unknown')
    away_team = event_data.get('awayTeam', {}).get('name', 'Unknown')
    
    print(f"\n⚽ {home_team} vs {away_team}")
    
    # Procesar alineaciones
    lineups = process_lineups(event_data)
    
    if not lineups:
        print("❌ No se encontraron alineaciones")
        return
    
    total_jugadores = len(lineups)
    print(f"\n👥 Total jugadores en el partido: {total_jugadores}")
    
    # Diagnosticar cada jugador
    for i, jugador in enumerate(lineups, 1):
        print(f"\n{'─'*80}")
        print(f"Jugador {i}/{total_jugadores}")
        diagnosticar_jugador(
            jugador['Nombre'],
            jugador['Dorsal'],
            jugador['Equipo']
        )


if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🔍 HERRAMIENTA DE DIAGNÓSTICO                             ║
║                    Sistema de Detección de Jugadores                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("\nOpciones:")
    print("1. Diagnosticar un jugador específico")
    print("2. Diagnosticar todos los jugadores de un partido")
    
    opcion = input("\nSelecciona una opción (1 o 2): ").strip()
    
    if opcion == "1":
        nombre = input("Nombre del jugador: ").strip()
        dorsal = input("Dorsal: ").strip()
        equipo = input("Equipo: ").strip()
        
        diagnosticar_jugador(nombre, dorsal, equipo)
    
    elif opcion == "2":
        match_id = input("Match ID: ").strip()
        diagnosticar_partido(match_id)
    
    else:
        print("❌ Opción no válida")
