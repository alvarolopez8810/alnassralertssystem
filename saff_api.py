"""
Módulo para extraer datos de partidos desde SAFF+ API
Adaptado del código de extracción de SAFF+ para obtener lineups de partidos
"""

import requests
import pandas as pd
import json
import re
from typing import Optional, Dict, List, Tuple

BEARER_TOKEN = "5O1SNE9VGH62MA16F2G088VJSV33FLF6"

API_HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Origin": "https://saffplus.sa",
    "Referer": "https://saffplus.sa/",
    "Accept": "*/*"
}

URL_EVENT_DETAILS = "https://cda.mottostreaming.com/motto.cda.cms.event.v1.EventService/GetEvent"
URL_ANNOTATIONS = "https://cda.mottostreaming.com/motto.cda.annotations.annotation.v1.AnnotationService/ListAnnotations"


def extraer_match_id_de_url(url: str) -> Optional[str]:
    """
    Extrae el match ID de una URL de SAFF+
    
    Ejemplos de URLs:
    - https://saffplus.sa/match/ABC123XYZ
    - https://saffplus.sa/event/ABC123XYZ
    
    Args:
        url: URL del partido
    
    Returns:
        Match ID o None si no se encuentra
    """
    patterns = [
        r'/match/([A-Za-z0-9_-]+)',
        r'/event/([A-Za-z0-9_-]+)',
        r'id=([A-Za-z0-9_-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    if '/' not in url and len(url) > 10:
        return url
    
    return None


def get_event_details(match_id: str) -> Optional[Dict]:
    """
    Obtiene los detalles de un evento/partido desde SAFF+ API
    
    Args:
        match_id: ID del partido
    
    Returns:
        Diccionario con los datos del evento o None si hay error
    """
    params_details = {
        "encoding": "json",
        "message": json.dumps({"eventId": match_id, "locale": "en"})
    }
    
    try:
        r = requests.get(URL_EVENT_DETAILS, headers=API_HEADERS, params=params_details, timeout=10)
        r.raise_for_status()
        return r.json().get("event")
    except Exception as e:
        print(f"Error obteniendo detalles del evento: {e}")
        return None


def extraer_info_partido(event_data: Dict) -> Dict:
    """
    Extrae información básica del partido
    
    Args:
        event_data: Datos del evento desde la API
    
    Returns:
        Diccionario con información del partido
    """
    fields = event_data.get("fields", {})
    
    home_club = fields.get("home_club", {}).get("item", {}).get("name", "N/A")
    away_club = fields.get("away_club", {}).get("item", {}).get("name", "N/A")
    
    start_time = event_data.get("startTime", "N/A")
    venue = fields.get("venue", {}).get("item", {}).get("name", "N/A")
    
    return {
        "match_id": event_data.get("id"),
        "home_team": home_club,
        "away_team": away_club,
        "start_time": start_time,
        "venue": venue,
        "title": event_data.get("name", "N/A")
    }


def process_lineups(event_data: Dict, match_id: str) -> List[Dict]:
    """
    Procesa las alineaciones del partido y extrae información de jugadores
    
    Args:
        event_data: Datos del evento desde la API
        match_id: ID del partido
    
    Returns:
        Lista de diccionarios con información de cada jugador
    """
    lineups = []
    fields = event_data.get("fields", {})
    
    player_lists = [
        ("home_starting_players", fields.get("home_club", {}).get("item", {}).get("name"), "Starting"),
        ("home_bench_players", fields.get("home_club", {}).get("item", {}).get("name"), "Substitute"),
        ("away_starting_players", fields.get("away_club", {}).get("item", {}).get("name"), "Starting"),
        ("away_bench_players", fields.get("away_club", {}).get("item", {}).get("name"), "Substitute"),
    ]
    
    for key, team_name, player_type in player_lists:
        player_entries = fields.get(key, [])
        
        for player_entry in player_entries:
            player_id = None
            if "id" in player_entry:
                player_id = player_entry.get("id")
            elif "item" in player_entry and isinstance(player_entry["item"], dict):
                player_id = player_entry["item"].get("id")
            
            item = player_entry.get("item", {})
            item_fields = item.get("fields", {})
            player_name = item.get("name") or player_entry.get("name", "N/A")
            birthday = item_fields.get("birthday", "N/A")
            nationality = item_fields.get("nationality", "N/A")
            
            if birthday != "N/A" and "T" in str(birthday):
                birthday = str(birthday).split("T")[0]
            
            lineups.append({
                "match_id": match_id,
                "player_id": player_id,
                "team": team_name,
                "player_name": player_name,
                "position": player_entry.get("position"),
                "jersey": player_entry.get("jersey_number"),
                "type": player_type,
                "birthday": birthday,
                "nationality": nationality
            })
    
    return lineups


def obtener_jugadores_partido(match_id_o_url: str) -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
    """
    Función principal para obtener los jugadores de un partido desde SAFF+
    
    Args:
        match_id_o_url: ID del partido o URL completa
    
    Returns:
        Tupla con (DataFrame de jugadores, información del partido)
        Retorna (None, None) si hay error
    """
    if match_id_o_url.startswith('http'):
        match_id = extraer_match_id_de_url(match_id_o_url)
        if not match_id:
            return None, None
    else:
        match_id = match_id_o_url
    
    event_data = get_event_details(match_id)
    
    if not event_data:
        return None, None
    
    info_partido = extraer_info_partido(event_data)
    
    lineups = process_lineups(event_data, match_id)
    
    if not lineups:
        return None, info_partido
    
    df_jugadores = pd.DataFrame(lineups)
    
    return df_jugadores, info_partido


def formatear_jugadores_para_busqueda(df_jugadores: pd.DataFrame) -> pd.DataFrame:
    """
    Formatea el DataFrame de jugadores para que sea compatible con el sistema de búsqueda
    
    Args:
        df_jugadores: DataFrame con jugadores desde SAFF+
    
    Returns:
        DataFrame formateado con las columnas esperadas por el sistema
    """
    df_formatted = pd.DataFrame()
    
    df_formatted['Nombre'] = df_jugadores['player_name']
    df_formatted['Equipo'] = df_jugadores['team']
    df_formatted['Dorsal'] = df_jugadores['jersey']
    df_formatted['Posicion'] = df_jugadores['position']
    df_formatted['Tipo'] = df_jugadores['type'].map({
        'Starting': 'Titular',
        'Substitute': 'Suplente'
    })
    df_formatted['Nationality'] = df_jugadores['nationality']
    df_formatted['Birth_Date'] = df_jugadores['birthday']
    
    def extraer_año(fecha):
        if pd.isna(fecha) or fecha == 'N/A':
            return 'N/A'
        fecha_str = str(fecha)
        if len(fecha_str) >= 4:
            return fecha_str[:4]
        return 'N/A'
    
    df_formatted['Año_Nacimiento'] = df_jugadores['birthday'].apply(extraer_año)
    
    return df_formatted
