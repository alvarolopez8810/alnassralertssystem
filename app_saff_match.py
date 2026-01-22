"""
Aplicación Streamlit para verificar jugadores destacados desde un partido de SAFF+
Permite introducir un URL o ID de partido y busca coincidencias en Google Sheets
"""

import streamlit as st
import pandas as pd
from saff_api import obtener_jugadores_partido, formatear_jugadores_para_busqueda
from buscar_coincidencias import buscar_coincidencias_en_todas_pestanas
from google_sheets import leer_todas_las_pestanas, obtener_nombres_pestanas
import os

st.set_page_config(
    page_title="SAFF+ Match Checker - Al Nassr FC",
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
    .player-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0066CC;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


def mostrar_jugador_destacado(jugador_info):
    """
    Muestra la información de un jugador destacado en formato profesional
    """
    with st.container():
        tipo_jugador = jugador_info.get('Tipo', 'Titular')
        tipo_en_ingles = 'STARTER' if tipo_jugador == 'Titular' else 'SUBSTITUTE'
        
        st.markdown(f"""
        <div class="player-card">
            <h3>⚽ {jugador_info['Nombre']} (#{jugador_info['Dorsal']}) - {jugador_info['Equipo']}</h3>
            <p><strong>Type:</strong> {tipo_en_ingles}</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        st.divider()


with st.sidebar:
    if os.path.exists("alnassr_200x200.png"):
        st.image("alnassr_200x200.png", width=150)
    st.title("Al Nassr FC")
    st.header("📖 Instructions")
    st.markdown("""
    1. Enter the SAFF+ match URL or ID
    2. Click "Check Match"
    3. Review highlighted players
    4. See if any tracked players are in the lineup
    
    ---
    
    ### 🔗 URL Examples:
    - `https://saffplus.sa/match/ABC123`
    - `https://saffplus.sa/event/XYZ789`
    - Or just the ID: `ABC123`
    
    ---
    
    ### 📊 Database:
    The system searches in:
    - Google Sheets (mreports youth)
    - All sheets automatically
    - Real-time data
    """)
    
    st.divider()
    
    st.info("💡 This tool checks SAFF+ matches against your scouting database")


col_logo, col_title = st.columns([1, 4])

with col_logo:
    if os.path.exists("alnassr_200x200.png"):
        st.image("alnassr_200x200.png", width=120)

with col_title:
    st.title("⚽ SAFF+ Match Checker")
    st.markdown("**Check if tracked players are in a SAFF+ match**")

st.divider()

try:
    with st.spinner("🔄 Connecting to Google Sheets database..."):
        sheet_names = obtener_nombres_pestanas()
    st.success(f"✅ Connected to Google Sheets ({len(sheet_names)} sheets found)")
except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    st.info("💡 Make sure the service account credentials are configured in Streamlit secrets")
    st.stop()

st.header("🔗 Enter Match URL or ID")

match_input = st.text_input(
    "SAFF+ Match URL or ID",
    placeholder="https://saffplus.sa/match/ABC123 or just ABC123",
    help="Enter the full URL or just the match ID from SAFF+"
)

if match_input:
    st.divider()
    
    if st.button("🔍 CHECK MATCH", type="primary", use_container_width=True):
        
        try:
            with st.spinner("⏳ Fetching match data from SAFF+ API..."):
                df_jugadores, info_partido = obtener_jugadores_partido(match_input)
            
            if df_jugadores is None or info_partido is None:
                st.error("❌ Could not retrieve match data. Please check the URL/ID and try again.")
                st.info("💡 Make sure the match ID is correct and the match exists in SAFF+")
                st.stop()
            
            st.success("✅ Match data retrieved successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🏠 **Home:** {info_partido['home_team']}")
                st.info(f"✈️ **Away:** {info_partido['away_team']}")
            with col2:
                st.info(f"🏟️ **Venue:** {info_partido['venue']}")
                st.info(f"📅 **Date:** {info_partido['start_time'][:10] if len(info_partido['start_time']) > 10 else info_partido['start_time']}")
            
            total_jugadores = len(df_jugadores)
            st.success(f"✅ {total_jugadores} players found in match lineup")
            
            with st.expander("👥 View all players in match"):
                st.dataframe(
                    df_jugadores[['player_name', 'team', 'jersey', 'position', 'type', 'nationality']],
                    use_container_width=True
                )
            
            st.divider()
            
            status_placeholder = st.empty()
            status_placeholder.info("📊 Loading Google Sheets database...")
            sheets_data = leer_todas_las_pestanas()
            
            status_placeholder.info("🔍 Searching for highlighted players...")
            
            df_formatted = formatear_jugadores_para_busqueda(df_jugadores)
            
            jugadores_encontrados = buscar_coincidencias_en_todas_pestanas(
                df_formatted, 
                sheets_data
            )
            status_placeholder.empty()
            
            if len(jugadores_encontrados) == 0:
                st.info("ℹ️ No highlighted players found in this match")
                st.markdown("""
                ### 📝 What does this mean?
                - None of the players in this match are currently in your scouting database
                - This could be a new match with players not yet tracked
                - Or the players in this match are not in your target list
                """)
            else:
                st.success("✅ Search completed!")
                
                col1, col2 = st.columns(2)
                col1.metric("📊 Players in Match", total_jugadores)
                col2.metric("⚽ Highlighted Players Found", len(jugadores_encontrados))
                
                st.divider()
                st.header("⚽ HIGHLIGHTED PLAYERS IN THIS MATCH")
                
                st.success(f"🎯 Found {len(jugadores_encontrados)} tracked player(s) in this match!")
                
                for jugador in jugadores_encontrados:
                    mostrar_jugador_destacado(jugador)
                
                st.balloons()
                
                st.divider()
                
                st.markdown("""
                ### 📧 Next Steps:
                - Review the highlighted players above
                - Check their performance in the match
                - Consider sending alerts if needed
                - Update your scouting reports
                """)
        
        except Exception as e:
            st.error(f"❌ Error processing match: {str(e)}")
            with st.expander("🔍 View error details"):
                st.exception(e)

else:
    st.info("👆 Please enter a match URL or ID to start")
    
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        ### System Workflow:
        
        1. **URL/ID Input**: Enter a SAFF+ match URL or ID
        2. **API Extraction**: The system fetches match data from SAFF+ API
        3. **Player Extraction**: Extracts all players from both teams (starters + substitutes)
        4. **Database Search**: Searches for matches in your Google Sheets database
        5. **Matching Criteria**:
           - Player number (exact match)
           - Player name (85%+ similarity)
           - Team name (partial match)
        6. **Results Display**: Shows which tracked players are in the match
        
        ### Match Information Displayed:
        - Home and away teams
        - Venue and date
        - Complete lineup (starters and substitutes)
        - Player details (name, number, position, nationality)
        
        ### Highlighted Player Information:
        - Player name, team, and number
        - Position (from SAFF+) and Spec. Position (from database)
        - Nationality and League
        - Birth year
        - Performance level
        - Scout decision
        - Database sheet location
        """)
    
    with st.expander("🔗 Where to find match URLs"):
        st.markdown("""
        ### Finding SAFF+ Match URLs:
        
        1. Go to [saffplus.sa](https://saffplus.sa)
        2. Navigate to the match you want to check
        3. Copy the URL from your browser
        4. Paste it here
        
        **URL Format Examples:**
        - `https://saffplus.sa/match/V92ZUHBHk21ociydW9xhI`
        - `https://saffplus.sa/event/FXSzaQsIp8v0y6aXcRAwf`
        
        **Or just use the ID:**
        - `V92ZUHBHk21ociydW9xhI`
        - `FXSzaQsIp8v0y6aXcRAwf`
        """)

st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <em>SAFF+ Match Checker - Al Nassr FC Youth Scouting Department</em><br>
    <em>Powered by Python, Streamlit & SAFF+ API</em>
</div>
""", unsafe_allow_html=True)
