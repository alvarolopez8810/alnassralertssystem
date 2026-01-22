from pdf_parser import extraer_jugadores_pdf
from buscar_coincidencias import buscar_coincidencias_en_todas_pestanas
from config import EMAIL_USER, EMAIL_PASSWORD
import yagmail

pdf_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/Acta2AlNassr.pdf'
excel_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/mreportsyouth.xlsx'

print("Extrayendo jugadores del PDF...")
df_jugadores = extraer_jugadores_pdf(pdf_path)

print("Buscando coincidencias en Excel...")
jugadores_encontrados = buscar_coincidencias_en_todas_pestanas(df_jugadores, excel_path)

jugador_matari = None
for j in jugadores_encontrados:
    if 'MATARI' in j['Nombre'].upper():
        jugador_matari = j
        break

if jugador_matari:
    print(f"\nJugador encontrado: {jugador_matari['Nombre']}")
    print(f"Position (PDF): {jugador_matari['Posicion']}")
    print(f"Spec. Position (Excel): {jugador_matari.get('Spec_Position', 'N/A')}")
    print(f"Nationality: {jugador_matari.get('Nationality', 'N/A')}")
    print(f"League: {jugador_matari.get('League', 'N/A')}")
    print(f"\nEnviando email a rafitagil1975@gmail.com y rafitagil@hotmail.com...")
    
    tipo_jugador = jugador_matari.get('Tipo', 'Titular')
    tipo_en_ingles = 'STARTER' if tipo_jugador == 'Titular' else 'SUBSTITUTE'
    
    asunto = f"🚨 ALERT: {jugador_matari['Nombre']} ({jugador_matari['Equipo']}) - {tipo_en_ingles}"
    
    cuerpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px;">
        <h2 style="color: #0066cc; margin: 0; padding: 0; line-height: 1.2;">⚽ PLAYER IN THE LINE UP ({tipo_en_ingles})</h2><table style="border-collapse: collapse; width: 100%; max-width: 600px; margin: 0; padding: 0;">
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5; width: 140px;"><strong>Name:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari['Nombre']}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Team:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari['Equipo']}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Number:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari['Dorsal']}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Position:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari['Posicion']}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Spec. Position:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari.get('Spec_Position', 'Not specified')}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Nationality:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari.get('Nationality', 'Not specified')}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>League:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari.get('League', 'Not specified')}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Birth Year:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari['Año_Nacimiento']}</td>
            </tr>
            <tr>
                <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Performance:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_matari['Performance']}</td>
            </tr>
            <tr style="background-color: #fff3cd;">
                <td style="padding: 6px 10px; border: 1px solid #ddd;"><strong>Scout Decision:</strong></td>
                <td style="padding: 6px 10px; border: 1px solid #ddd;"><strong>{jugador_matari['Decisión']}</strong></td>
            </tr>
        </table>
        
        <p style="margin-top: 15px; color: #666; font-size: 12px;">
            <em>Automated alert system - Al Nassr FC</em>
        </p>
    </body>
    </html>
    """
    
    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
        destinatarios = ['rafitagil1975@gmail.com', 'rafitagil@hotmail.com']
        yag.send(
            to=destinatarios,
            subject=asunto,
            contents=cuerpo
        )
        print(f"✅ Email enviado exitosamente a {len(destinatarios)} destinatarios")
        for dest in destinatarios:
            print(f"   • {dest}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ No se encontró a MATARI")
