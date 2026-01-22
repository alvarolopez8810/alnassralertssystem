import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
import json
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

SPREADSHEET_ID = '1HssweG6CwbKejAb6jACCWu9MtYcqakuePXZYlBhxgxg'

def get_google_sheets_client():
    """
    Conecta con Google Sheets usando credenciales de múltiples fuentes:
    1. Variables de entorno individuales (Render)
    2. Streamlit secrets
    3. Archivo service_account.json local
    """
    try:
        credentials_dict = None
        
        if os.getenv('GCP_TYPE'):
            credentials_dict = {
                "type": os.getenv('GCP_TYPE'),
                "project_id": os.getenv('GCP_PROJECT_ID'),
                "private_key_id": os.getenv('GCP_PRIVATE_KEY_ID'),
                "private_key": os.getenv('GCP_PRIVATE_KEY'),
                "client_email": os.getenv('GCP_CLIENT_EMAIL'),
                "client_id": os.getenv('GCP_CLIENT_ID'),
                "auth_uri": os.getenv('GCP_AUTH_URI'),
                "token_uri": os.getenv('GCP_TOKEN_URI'),
                "auth_provider_x509_cert_url": os.getenv('GCP_AUTH_PROVIDER_X509_CERT_URL'),
                "client_x509_cert_url": os.getenv('GCP_CLIENT_X509_CERT_URL'),
                "universe_domain": os.getenv('GCP_UNIVERSE_DOMAIN', 'googleapis.com')
            }
        elif hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            credentials_dict = dict(st.secrets['gcp_service_account'])
        elif os.path.exists('service_account.json'):
            with open('service_account.json', 'r') as f:
                credentials_dict = json.load(f)
        else:
            raise Exception("No credentials found. Please configure GCP_* environment variables or Streamlit secrets.")
        
        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        
        client = gspread.authorize(credentials)
        return client
    
    except Exception as e:
        raise Exception(f"Error connecting to Google Sheets: {str(e)}")


@st.cache_data(ttl=300)
def leer_todas_las_pestanas():
    """
    Lee todas las pestañas del Google Sheet y las devuelve como un diccionario de DataFrames
    Similar a pd.ExcelFile pero para Google Sheets
    Cache de 5 minutos para mejorar rendimiento
    
    Returns:
        dict: {nombre_pestaña: DataFrame}
    """
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        todas_las_pestanas = {}
        
        for worksheet in spreadsheet.worksheets():
            sheet_name = worksheet.title
            
            data = worksheet.get_all_values()
            
            if len(data) > 0:
                df = pd.DataFrame(data[1:], columns=data[0])
                
                df = df.replace('', pd.NA)
                
                todas_las_pestanas[sheet_name] = df
        
        return todas_las_pestanas
    
    except Exception as e:
        raise Exception(f"Error reading Google Sheets: {str(e)}")


def leer_pestaña(nombre_pestaña):
    """
    Lee una pestaña específica del Google Sheet
    
    Args:
        nombre_pestaña: Nombre de la pestaña a leer
    
    Returns:
        DataFrame con los datos de la pestaña
    """
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(nombre_pestaña)
        
        data = worksheet.get_all_values()
        
        if len(data) > 0:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df.replace('', pd.NA)
            return df
        else:
            return pd.DataFrame()
    
    except Exception as e:
        raise Exception(f"Error reading sheet '{nombre_pestaña}': {str(e)}")


def obtener_nombres_pestanas():
    """
    Obtiene la lista de nombres de todas las pestañas
    
    Returns:
        list: Lista de nombres de pestañas
    """
    try:
        client = get_google_sheets_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        return [ws.title for ws in spreadsheet.worksheets()]
    
    except Exception as e:
        raise Exception(f"Error getting sheet names: {str(e)}")
