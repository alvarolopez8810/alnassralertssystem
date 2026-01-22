import yagmail
from config import EMAIL_USER, EMAIL_PASSWORD, EMAIL_DESTINATARIOS

def enviar_alerta_jugador(jugador_info):
    """
    Envía email de alerta cuando un jugador destacado es convocado
    
    Args:
        jugador_info: dict con datos del jugador
            - Nombre
            - Equipo
            - Dorsal
            - Decisión
            - (Opcional) Posición, Tipo, Performance, Watch, Scout, Año_Nacimiento, Partido
    """
    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
        
        tipo_jugador = jugador_info.get('Tipo', 'Titular')
        tipo_en_ingles = 'STARTER' if tipo_jugador == 'Titular' else 'SUBSTITUTE'
        
        asunto = f"🚨 ALERT: {jugador_info['Nombre']} ({jugador_info['Equipo']}) - {tipo_en_ingles}"
        
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px;">
            <h2 style="color: #0066cc; margin: 0; padding: 0; line-height: 1.2;">⚽ PLAYER IN THE LINE UP ({tipo_en_ingles})</h2><table style="border-collapse: collapse; width: 100%; max-width: 600px; margin: 0; padding: 0;">
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5; width: 140px;"><strong>Name:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Nombre']}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Team:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Equipo']}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Number:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Dorsal']}</td>
                </tr>"""
        
        if 'Posicion' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Position:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Posicion']}</td>
                </tr>"""
        
        if 'Spec_Position' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Spec. Position:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Spec_Position']}</td>
                </tr>"""
        
        if 'Nationality' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Nationality:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Nationality']}</td>
                </tr>"""
        
        if 'League' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>League:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['League']}</td>
                </tr>"""
        
        if 'Año_Nacimiento' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Birth Year:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Año_Nacimiento']}</td>
                </tr>"""
        
        if 'Performance' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Performance:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Performance']}</td>
                </tr>"""
        
        if 'Partido' in jugador_info:
            cuerpo += f"""
                <tr>
                    <td style="padding: 6px 10px; border: 1px solid #ddd; background-color: #f5f5f5;"><strong>Match:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;">{jugador_info['Partido']}</td>
                </tr>"""
        
        cuerpo += f"""
                <tr style="background-color: #fff3cd;">
                    <td style="padding: 6px 10px; border: 1px solid #ddd;"><strong>Scout Decision:</strong></td>
                    <td style="padding: 6px 10px; border: 1px solid #ddd;"><strong>{jugador_info['Decisión']}</strong></td>
                </tr>
            </table>
            
            <p style="margin-top: 15px; color: #666; font-size: 12px;">
                <em>Automated alert system - Al Nassr FC</em>
            </p>
        </body>
        </html>
        """
        
        yag.send(
            to=EMAIL_DESTINATARIOS,
            subject=asunto,
            contents=cuerpo
        )
        
        print(f"✅ Alerta enviada para {jugador_info['Nombre']} a {len(EMAIL_DESTINATARIOS)} destinatarios")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email: {str(e)}")
        return False


def test_email():
    """Función para probar que el email funciona"""
    jugador_test = {
        'Nombre': 'Test Player',
        'Equipo': 'Al Nassr U19',
        'Dorsal': 10,
        'Decisión': 'SEGUIR'
    }
    
    return enviar_alerta_jugador(jugador_test)


if __name__ == "__main__":
    test_email()
