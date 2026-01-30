import pandas as pd
import re
from difflib import SequenceMatcher

def normalizar_nombre(nombre):
    """
    Normaliza un nombre para comparación:
    - Convierte a mayúsculas
    - Elimina espacios extras
    - Elimina caracteres especiales
    """
    if pd.isna(nombre):
        return ""
    nombre = str(nombre).upper().strip()
    nombre = re.sub(r'\s+', ' ', nombre)
    nombre = re.sub(r'[^\w\s]', '', nombre)
    return nombre


def normalizar_equipo(equipo):
    """
    Normaliza nombres de equipos para comparación
    """
    if pd.isna(equipo):
        return ""
    equipo = str(equipo).upper().strip()
    
    # Eliminar sufijos comunes
    equipo = equipo.replace(' FC', '').replace(' SFC', '').replace(' CLUB', '').strip()
    
    # Eliminar guiones y normalizar espacios
    equipo = equipo.replace('-', ' ')
    equipo = re.sub(r'\s+', ' ', equipo)
    
    # Mapeo de variaciones comunes
    mapeo_equipos = {
        'AL NASSR': 'AL NASSR',
        'ALNASSR': 'AL NASSR',
        'AL ITTIHAD': 'AL ITTIHAD',
        'ALITTIHAD': 'AL ITTIHAD',
        'AL HILAL': 'AL HILAL',
        'ALHILAL': 'AL HILAL',
        'AL AHLI': 'AL AHLI',
        'ALAHLI': 'AL AHLI',
        'AL RAED': 'AL RAED',
        'ALRAED': 'AL RAED',
        'AL RAYED': 'AL RAED',
        'AL QADSIAH': 'AL QADSIAH',
        'ALQADSIAH': 'AL QADSIAH',
    }
    
    for key, value in mapeo_equipos.items():
        if key in equipo:
            return value
    
    return equipo


def similitud_nombres(nombre1, nombre2):
    """
    Calcula similitud entre dos nombres (0 a 1)
    """
    return SequenceMatcher(None, nombre1, nombre2).ratio()


def buscar_jugador_en_excel(jugador_pdf, df_excel):
    """
    Busca un jugador del PDF en el DataFrame del Excel
    
    Args:
        jugador_pdf: dict con datos del jugador del PDF (Nombre, Dorsal, Equipo)
        df_excel: DataFrame del Excel con columnas Name, Number, Team
    
    Returns:
        dict con resultado de la búsqueda o None si no hay coincidencia
    """
    nombre_pdf = normalizar_nombre(jugador_pdf['Nombre'])
    dorsal_pdf = jugador_pdf['Dorsal']
    equipo_pdf = normalizar_equipo(jugador_pdf['Equipo'])
    
    # Extraer primer nombre para comparación parcial
    primer_nombre_pdf = nombre_pdf.split()[0] if nombre_pdf else ""
    
    for idx, row in df_excel.iterrows():
        nombre_excel = normalizar_nombre(row.get('Name', ''))
        dorsal_excel = row.get('Number', None)
        equipo_excel = normalizar_equipo(row.get('Team', ''))
        
        # Verificar coincidencia de dorsal
        coincide_dorsal = False
        if pd.notna(dorsal_excel):
            try:
                coincide_dorsal = int(dorsal_excel) == int(dorsal_pdf)
            except:
                pass
        
        # Verificar coincidencia de equipo
        coincide_equipo = equipo_pdf in equipo_excel or equipo_excel in equipo_pdf
        
        # Calcular similitud de nombre completo
        similitud = similitud_nombres(nombre_pdf, nombre_excel)
        
        # Verificar si el nombre del PDF está contenido en el nombre del Excel
        nombre_contenido = nombre_pdf in nombre_excel
        
        # Verificar si el primer nombre coincide (para casos como "FERAS" vs "FERAS SULAIMAN ALRAJHI")
        nombre_excel_parts = nombre_excel.split() if nombre_excel else []
        primer_nombre_excel = nombre_excel_parts[0] if nombre_excel_parts else ""
        coincide_primer_nombre = primer_nombre_pdf == primer_nombre_excel if primer_nombre_pdf else False
        
        # CRITERIO 1: Dorsal + Equipo + Nombre similar (>70%)
        if coincide_dorsal and coincide_equipo and similitud > 0.7:
            return {
                'encontrado': True,
                'fila_excel': idx,
                'datos_excel': row.to_dict(),
                'similitud_nombre': similitud,
                'coincide_dorsal': coincide_dorsal,
                'coincide_equipo': coincide_equipo
            }
        
        # CRITERIO 2: Dorsal + Equipo + Primer nombre coincide (para nombres parciales)
        if coincide_dorsal and coincide_equipo and coincide_primer_nombre:
            return {
                'encontrado': True,
                'fila_excel': idx,
                'datos_excel': row.to_dict(),
                'similitud_nombre': similitud,
                'coincide_dorsal': coincide_dorsal,
                'coincide_equipo': coincide_equipo
            }
        
        # CRITERIO 3: Dorsal + Equipo + Nombre contenido
        if coincide_dorsal and coincide_equipo and nombre_contenido:
            return {
                'encontrado': True,
                'fila_excel': idx,
                'datos_excel': row.to_dict(),
                'similitud_nombre': similitud,
                'coincide_dorsal': coincide_dorsal,
                'coincide_equipo': coincide_equipo
            }
        
        # CRITERIO 4: Nombre muy similar (>85%) + Equipo
        elif similitud > 0.85 and coincide_equipo:
            return {
                'encontrado': True,
                'fila_excel': idx,
                'datos_excel': row.to_dict(),
                'similitud_nombre': similitud,
                'coincide_dorsal': coincide_dorsal,
                'coincide_equipo': coincide_equipo
            }
    
    return None


def buscar_coincidencias_en_todas_pestanas(df_jugadores_pdf, sheets_dict=None):
    """
    Busca coincidencias en todas las pestañas del Google Sheet o Excel
    
    Args:
        df_jugadores_pdf: DataFrame con jugadores del PDF
        sheets_dict: dict con {nombre_pestaña: DataFrame} o None para usar Excel local
    
    Returns:
        list de dicts con jugadores encontrados y sus datos
    """
    jugadores_encontrados = []
    
    if sheets_dict is None:
        excel_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/mreportsyouth.xlsx'
        xls = pd.ExcelFile(excel_path)
        sheet_names = xls.sheet_names
        def get_sheet(name):
            return pd.read_excel(excel_path, sheet_name=name)
    else:
        sheet_names = sheets_dict.keys()
        def get_sheet(name):
            return sheets_dict[name]
    
    for sheet_name in sheet_names:
        df_sheet = get_sheet(sheet_name)
        
        if 'Name' not in df_sheet.columns or 'Number' not in df_sheet.columns:
            continue
        
        for idx, jugador_pdf in df_jugadores_pdf.iterrows():
            resultado = buscar_jugador_en_excel(jugador_pdf, df_sheet)
            
            if resultado:
                spec_position = resultado['datos_excel'].get('Spec. Position', None)
                if not spec_position or pd.isna(spec_position):
                    spec_position = 'Not specified'
                
                jugador_info = {
                    'Nombre': jugador_pdf['Nombre'],
                    'Equipo': jugador_pdf['Equipo'],
                    'Dorsal': jugador_pdf['Dorsal'],
                    'Posicion': jugador_pdf['Posicion'],
                    'Spec_Position': spec_position,
                    'Tipo': jugador_pdf['Tipo'],
                    'Año_Nacimiento': jugador_pdf['Año_Nacimiento'],
                    'Nationality': resultado['datos_excel'].get('Nationality', 'Not specified'),
                    'League': resultado['datos_excel'].get('League', 'Not specified'),
                    'Pestaña_Excel': sheet_name,
                    'Decisión': resultado['datos_excel'].get('Profile Decision', 'No especificada'),
                    'Performance': resultado['datos_excel'].get('Performance', 'No especificada'),
                    'Watch': resultado['datos_excel'].get('Watch', 'No especificada'),
                    'Scout': resultado['datos_excel'].get('Scout', 'No especificado'),
                    'similitud': resultado['similitud_nombre']
                }
                
                jugadores_encontrados.append(jugador_info)
    
    return jugadores_encontrados
