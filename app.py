import streamlit as st
import pandas as pd
from pdf_parser import extraer_jugadores_pdf, extraer_info_partido
from saff_api import obtener_jugadores_partido, formatear_jugadores_para_busqueda
from buscar_coincidencias import buscar_coincidencias_en_todas_pestanas
from email_alertas import enviar_alerta_jugador
from google_sheets import leer_todas_las_pestanas, obtener_nombres_pestanas
from config import EMAIL_DESTINATARIOS
from PIL import Image
import os
import tempfile

st.set_page_config(
    page_title="Al Nassr FC - Sistema de Alertas",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stButton>button {
        background-color: #0066CC;
        color: white;
        font-weight: bold;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004A99;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    h1 {
        color: #0066CC;
    }
    h2 {
        color: #0066CC;
    }
    h3 {
        color: #004A99;
    }
</style>
""", unsafe_allow_html=True)

def mostrar_jugador_destacado(jugador_info, email_enviado):
    """
    Muestra la información de un jugador destacado en formato profesional
    """
    with st.container():
        tipo_jugador = jugador_info.get('Tipo', 'Titular')
        tipo_en_ingles = 'STARTER' if tipo_jugador == 'Titular' else 'SUBSTITUTE'
        
        st.markdown(f"### ⚽ {jugador_info['Nombre']} (#{jugador_info['Dorsal']}) - {jugador_info['Equipo']}")
        st.markdown(f"**Type:** {tipo_en_ingles}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            * **Position:** {jugador_info.get('Posicion', 'N/A')}
            * **Spec. Position:** {jugador_info.get('Spec_Position', 'N/A')}
            * **Nationality:** {jugador_info.get('Nationality', 'N/A')}
            * **League:** {jugador_info.get('League', 'N/A')}
            """)
        
        with col2:
            st.markdown(f"""
            * **Birth Year:** {jugador_info.get('Año_Nacimiento', 'N/A')}
            * **Performance:** {jugador_info.get('Performance', 'N/A')}
            * **Scout Decision:** {jugador_info.get('Decisión', 'N/A')}
            * **Excel Sheet:** {jugador_info.get('Pestaña_Excel', 'N/A')}
            """)
        
        if email_enviado:
            st.success("✉️ Alert sent successfully")
        else:
            st.error("❌ Error sending alert")
        
        st.divider()


with st.sidebar:
    st.image("alnassr_200x200.png", width=150)
    st.title("Al Nassr FC")
    st.header("📖 Instructions")
    st.markdown("""
    **Choose your input method:**
    
    1. **PDF Upload**: Upload match lineup PDF
    2. **SAFF+ URL**: Enter match URL or ID
    
    Then:
    - Click "Process and Send Alerts"
    - Review highlighted players
    - Send email alerts if needed
    
    ---
    
    ### 📧 Email Recipients:
    - al.scoutinglab@gmail.com
    - rafitagil1975@gmail.com
    - rafitagil@hotmail.com
    
    ---
    
    ### 📊 Database:
    The system searches in:
    - Google Sheets (Cloud)
    - All sheets automatically
    - Real-time data
    """)
    
    st.divider()
    
    modo_prueba = st.checkbox("🧪 Test Mode (no emails)")
    if modo_prueba:
        st.warning("⚠️ Test mode active - emails will NOT be sent")

col_logo, col_title = st.columns([1, 4])

with col_logo:
    if os.path.exists("alnassr_200x200.png"):
        st.image("alnassr_200x200.png", width=120)

with col_title:
    st.title("⚽ Al Nassr FC - Player Alert System")
    st.markdown("**Automated scouting alert system for youth categories**")

st.divider()

st.header("📥 Select Input Method")

input_method = st.radio(
    "Choose how to input match data:",
    ["📄 Upload PDF", "🔗 SAFF+ URL/ID"],
    horizontal=True
)

st.divider()

uploaded_file = None
match_input = None

if input_method == "📄 Upload PDF":
    st.subheader("📄 Upload Match Lineup (PDF)")
    uploaded_file = st.file_uploader(
        "Select the match lineup PDF file",
        type=['pdf'],
        help="Upload the official match lineup PDF from MySAFF system"
    )
else:
    st.subheader("🔗 Enter SAFF+ Match URL or ID")
    match_input = st.text_input(
        "SAFF+ Match URL or ID",
        placeholder="https://saffplus.sa/match/ABC123 or just ABC123",
        help="Enter the full URL or just the match ID from SAFF+"
    )
    if match_input:
        st.success(f"✅ Match ID/URL entered: {match_input}")

try:
    with st.spinner("🔄 Connecting to Google Sheets database..."):
        sheet_names = obtener_nombres_pestanas()
    st.success(f"✅ Connected to Google Sheets ({len(sheet_names)} sheets found)")
except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    st.info("💡 Make sure the service account credentials are configured in Streamlit secrets")
    st.stop()

if uploaded_file is not None or match_input:
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_temp_path = tmp_file.name
    
    st.divider()
    
    if st.button("🔔 PROCESS AND SEND ALERTS", type="primary", use_container_width=True):
        
        try:
            if uploaded_file:
                with st.spinner("⏳ Extracting match information from PDF..."):
                    info_partido = extraer_info_partido(pdf_temp_path)
                
                st.info(f"📋 **Match #{info_partido['ID_Partido']}** - {info_partido['Fecha']} at {info_partido['Hora']}")
                st.info(f"🏟️ **Stadium:** {info_partido['Estadio']}")
                
                with st.spinner("⏳ Processing lineup..."):
                    df_jugadores = extraer_jugadores_pdf(pdf_temp_path)
                    total_jugadores = len(df_jugadores)
                    
                match_info_display = f"#{info_partido['ID_Partido']} - {info_partido['Fecha']}"
            
            else:
                with st.spinner("⏳ Fetching match data from SAFF+ API..."):
                    df_jugadores_saff, info_partido_saff = obtener_jugadores_partido(match_input)
                
                if df_jugadores_saff is None or info_partido_saff is None:
                    st.error("❌ Could not retrieve match data. Please check the URL/ID and try again.")
                    st.stop()
                
                st.success("✅ Match data retrieved from SAFF+!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"🏠 **Home:** {info_partido_saff['home_team']}")
                    st.info(f"✈️ **Away:** {info_partido_saff['away_team']}")
                with col2:
                    st.info(f"🏟️ **Venue:** {info_partido_saff['venue']}")
                    st.info(f"📅 **Date:** {info_partido_saff['start_time'][:10] if len(info_partido_saff['start_time']) > 10 else info_partido_saff['start_time']}")
                
                df_jugadores = formatear_jugadores_para_busqueda(df_jugadores_saff)
                total_jugadores = len(df_jugadores)
                
                match_info_display = f"{info_partido_saff['home_team']} vs {info_partido_saff['away_team']} - {info_partido_saff['start_time'][:10]}"
            
            st.success(f"✅ {total_jugadores} players extracted from PDF")
            
            status_placeholder = st.empty()
            status_placeholder.info("📊 Loading Google Sheets database...")
            sheets_data = leer_todas_las_pestanas()
            
            status_placeholder.info("🔍 Searching for highlighted players...")
            jugadores_encontrados = buscar_coincidencias_en_todas_pestanas(
                df_jugadores, 
                sheets_data
            )
            status_placeholder.empty()
            
            if len(jugadores_encontrados) == 0:
                st.info("ℹ️ No highlighted players found in this lineup")
            else:
                st.success("✅ Processing completed!")
                
                col1, col2 = st.columns(2)
                col1.metric("📊 Players Analyzed", total_jugadores)
                col2.metric("⚽ Highlighted Players", len(jugadores_encontrados))
                
                st.divider()
                st.header("⚽ HIGHLIGHTED PLAYERS")
                
                for jugador in jugadores_encontrados:
                    mostrar_jugador_destacado(jugador, False)
                
                st.divider()
                
                if not modo_prueba:
                    st.warning(f"🔔 {len(jugadores_encontrados)} highlighted players found!")
                    
                    if st.button("📧 Send Email Alerts", type="primary", use_container_width=True):
                        alertas_enviadas = 0
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, jugador in enumerate(jugadores_encontrados):
                            status_text.info(f"📧 Sending email {i+1}/{len(jugadores_encontrados)}: {jugador['Nombre']}...")
                            progress_bar.progress((i + 1) / len(jugadores_encontrados))
                            
                            jugador_info = {
                                'Nombre': jugador['Nombre'],
                                'Equipo': jugador['Equipo'],
                                'Dorsal': jugador['Dorsal'],
                                'Decisión': jugador['Decisión'],
                                'Posicion': jugador['Posicion'],
                                'Spec_Position': jugador.get('Spec_Position', 'Not specified'),
                                'Tipo': jugador['Tipo'],
                                'Performance': jugador['Performance'],
                                'Nationality': jugador.get('Nationality', 'Not specified'),
                                'League': jugador.get('League', 'Not specified'),
                                'Año_Nacimiento': jugador['Año_Nacimiento'],
                                'Partido': match_info_display
                            }
                            
                            email_enviado = enviar_alerta_jugador(jugador_info)
                            
                            if email_enviado:
                                alertas_enviadas += 1
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        st.balloons()
                        st.success(f"🎉 {alertas_enviadas} alerts sent successfully to {EMAIL_DESTINATARIOS[0]}!")
                else:
                    st.info("🧪 Test mode: Review players above. No emails will be sent.")
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            with st.expander("🔍 View error details"):
                st.exception(e)
        
        finally:
            if uploaded_file and os.path.exists(pdf_temp_path):
                os.unlink(pdf_temp_path)

else:
    st.info("👆 Please select an input method and provide match data to start")
    
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        ### System Workflow:
        
        **Option 1: PDF Upload**
        1. Upload the official match lineup PDF
        2. System extracts all players from the PDF
        3. Searches for matches in Google Sheets database
        
        **Option 2: SAFF+ URL/ID**
        1. Enter SAFF+ match URL or ID
        2. System fetches data directly from SAFF+ API
        3. Searches for matches in Google Sheets database
        
        **Matching Criteria:**
        - Player number (exact match)
        - Player name (85%+ similarity)
        - Team name (partial match)
        
        **Email Alerts:**
        - Sends formatted emails to all recipients
        - Includes player details, performance, and scout decision
        
        ### Email Content:
        - Player name, team, and number
        - Position (generic and specific)
        - Nationality and League
        - Birth year
        - Performance level
        - Scout decision
        - Match information
        """)
    
    with st.expander("🔗 SAFF+ URL Examples"):
        st.markdown("""
        ### Valid SAFF+ URLs:
        - `https://saffplus.sa/match/V92ZUHBHk21ociydW9xhI`
        - `https://saffplus.sa/event/FXSzaQsIp8v0y6aXcRAwf`
        
        ### Or just the ID:
        - `V92ZUHBHk21ociydW9xhI`
        - `FXSzaQsIp8v0y6aXcRAwf`
        """)

st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <em>Automated Alert System - Al Nassr FC Youth Scouting Department</em><br>
    <em>Powered by Python, Streamlit & AI</em>
</div>
""", unsafe_allow_html=True)
