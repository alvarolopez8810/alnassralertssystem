import fitz
import pandas as pd
import re

def extraer_jugadores_pdf(pdf_path):
    """
    Extrae información de jugadores desde un PDF de acta de partido
    
    Returns:
        DataFrame con columnas: Equipo, Nombre, Año_Nacimiento, Posicion, Dorsal, Tipo
    """
    pdf_document = fitz.open(pdf_path)
    
    full_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        full_text += page.get_text()
    
    pdf_document.close()
    
    jugadores = []
    lineas = full_text.split('\n')
    
    contador_jugador = 0
    
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        if "Team coach" in linea or "Match Officials" in linea or "Match O!cials" in linea:
            break
        
        match_nombre = re.search(r'^(.+?)\s+\((\d{4})\)', linea)
        
        if match_nombre:
            nombre = match_nombre.group(1).strip()
            anio = int(match_nombre.group(2))
            nombre = re.sub(r'\s*\(C\)\s*', '', nombre).strip()
            
            posicion = None
            dorsal = None
            
            for offset in range(1, 8):
                if i + offset >= len(lineas):
                    break
                
                linea_siguiente = lineas[i + offset].strip()
                
                if linea_siguiente == '(C)':
                    continue
                
                if linea_siguiente in ['GK', 'DF', 'MF', 'FW']:
                    posicion = linea_siguiente
                    
                    if i + offset + 1 < len(lineas):
                        linea_dorsal = lineas[i + offset + 1].strip()
                        if linea_dorsal.isdigit():
                            dorsal = int(linea_dorsal)
                    break
            
            if posicion and dorsal:
                if contador_jugador <= 10:
                    equipo = "Al-Ittihad Club"
                    tipo = "Titular"
                elif contador_jugador <= 21:
                    equipo = "Al-Nassr FC"
                    tipo = "Titular"
                elif contador_jugador <= 29:
                    equipo = "Al-Ittihad Club"
                    tipo = "Suplente"
                else:
                    equipo = "Al-Nassr FC"
                    tipo = "Suplente"
                
                jugadores.append({
                    'Equipo': equipo,
                    'Nombre': nombre,
                    'Año_Nacimiento': anio,
                    'Posicion': posicion,
                    'Dorsal': dorsal,
                    'Tipo': tipo
                })
                
                contador_jugador += 1
        
        i += 1
    
    return pd.DataFrame(jugadores)


def extraer_info_partido(pdf_path):
    """
    Extrae información general del partido
    
    Returns:
        dict con información del partido
    """
    pdf_document = fitz.open(pdf_path)
    
    full_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        full_text += page.get_text()
    
    pdf_document.close()
    
    lineas = full_text.split('\n')
    
    estadio = lineas[8].strip() if len(lineas) > 8 else "No encontrado"
    duracion = lineas[9].strip() if len(lineas) > 9 else "No encontrada"
    fecha_hora = lineas[10].strip() if len(lineas) > 10 else "No encontrada"
    numero_partido = lineas[11].strip() if len(lineas) > 11 else "No encontrado"
    
    if fecha_hora:
        match_fecha = re.search(r'(\w+)\s*-\s*(\d+)\s+(\w+)\s*-\s*(\d+:\d+\s*[AP]M)', fecha_hora)
        if match_fecha:
            fecha = f"{match_fecha.group(1)} {match_fecha.group(2)} {match_fecha.group(3)}"
            hora = match_fecha.group(4)
        else:
            fecha = fecha_hora
            hora = "No encontrada"
    else:
        fecha = "No encontrada"
        hora = "No encontrada"
    
    return {
        'ID_Partido': numero_partido,
        'Fecha': fecha,
        'Hora': hora,
        'Estadio': estadio,
        'Duracion': duracion
    }
