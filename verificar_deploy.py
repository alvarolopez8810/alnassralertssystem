"""
Script para verificar que todos los archivos necesarios para Render están listos
"""
import os
import sys

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    
    archivos_necesarios = [
        'app_league_checker.py',
        'check_league_players.py',
        'saff_api.py',
        'google_sheets.py',
        'buscar_coincidencias.py',
        'email_resumen_liga.py',
        'config.py',
        'requirements.txt',
        '.streamlit/config.toml'
    ]
    
    archivos_opcionales = [
        'render.yaml',
        'DEPLOY_RENDER.md',
        'ARCHIVOS_PARA_RENDER.txt'
    ]
    
    print("=" * 80)
    print("🔍 VERIFICACIÓN DE ARCHIVOS PARA RENDER")
    print("=" * 80)
    
    print("\n✅ ARCHIVOS OBLIGATORIOS:")
    todos_presentes = True
    for archivo in archivos_necesarios:
        existe = os.path.exists(archivo)
        simbolo = "✅" if existe else "❌"
        print(f"   {simbolo} {archivo}")
        if not existe:
            todos_presentes = False
    
    print("\n📋 ARCHIVOS OPCIONALES:")
    for archivo in archivos_opcionales:
        existe = os.path.exists(archivo)
        simbolo = "✅" if existe else "⚪"
        print(f"   {simbolo} {archivo}")
    
    print("\n🔐 ARCHIVOS QUE NO DEBES SUBIR:")
    archivos_no_subir = ['.env', 'service_account.json', 'credentials.json']
    for archivo in archivos_no_subir:
        existe = os.path.exists(archivo)
        if existe:
            print(f"   ⚠️  {archivo} - NO subir a Render (usar variables de entorno)")
        else:
            print(f"   ✅ {archivo} - No encontrado (correcto)")
    
    print("\n" + "=" * 80)
    
    if todos_presentes:
        print("✅ TODOS LOS ARCHIVOS OBLIGATORIOS ESTÁN PRESENTES")
        print("\n📦 Próximos pasos:")
        print("   1. Sube estos archivos a tu repositorio Git")
        print("   2. Conecta el repositorio a Render")
        print("   3. Configura las variables de entorno en Render:")
        print("      - EMAIL_USER")
        print("      - EMAIL_PASSWORD")
        print("      - GCP_* (credenciales de Google)")
        print("   4. Despliega la aplicación")
        print("\n📖 Consulta DEPLOY_RENDER.md para instrucciones detalladas")
    else:
        print("❌ FALTAN ARCHIVOS OBLIGATORIOS")
        print("   Por favor, asegúrate de tener todos los archivos antes de desplegar")
        return False
    
    print("=" * 80)
    return True


def verificar_requirements():
    """Verifica que requirements.txt tenga todas las dependencias"""
    print("\n" + "=" * 80)
    print("📦 VERIFICACIÓN DE DEPENDENCIAS")
    print("=" * 80)
    
    dependencias_necesarias = [
        'streamlit',
        'yagmail',
        'python-dotenv',
        'pandas',
        'gspread',
        'google-auth',
        'requests'
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            contenido = f.read().lower()
        
        print("\n✅ Dependencias encontradas:")
        for dep in dependencias_necesarias:
            if dep.lower() in contenido:
                print(f"   ✅ {dep}")
            else:
                print(f"   ❌ {dep} - FALTA")
        
        print("\n" + "=" * 80)
        return True
    except FileNotFoundError:
        print("❌ requirements.txt no encontrado")
        return False


def verificar_config_streamlit():
    """Verifica que la configuración de Streamlit esté correcta"""
    print("\n" + "=" * 80)
    print("⚙️  VERIFICACIÓN DE CONFIGURACIÓN STREAMLIT")
    print("=" * 80)
    
    if os.path.exists('.streamlit/config.toml'):
        print("   ✅ .streamlit/config.toml existe")
        
        with open('.streamlit/config.toml', 'r') as f:
            contenido = f.read()
        
        if '[server]' in contenido:
            print("   ✅ Sección [server] configurada")
        else:
            print("   ⚠️  Sección [server] no encontrada")
        
        print("\n" + "=" * 80)
        return True
    else:
        print("   ❌ .streamlit/config.toml no encontrado")
        print("   Crea este archivo para configurar Streamlit")
        return False


if __name__ == "__main__":
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║           🚀 VERIFICACIÓN DE ARCHIVOS PARA DEPLOY EN RENDER                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    resultado1 = verificar_archivos()
    resultado2 = verificar_requirements()
    resultado3 = verificar_config_streamlit()
    
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                            📊 RESUMEN FINAL                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    if resultado1 and resultado2 and resultado3:
        print("\n✅ TODO LISTO PARA DESPLEGAR EN RENDER")
        print("\n📖 Lee DEPLOY_RENDER.md para instrucciones paso a paso")
        print("📋 Lee ARCHIVOS_PARA_RENDER.txt para un resumen rápido")
        sys.exit(0)
    else:
        print("\n⚠️  HAY PROBLEMAS QUE RESOLVER ANTES DE DESPLEGAR")
        print("   Revisa los mensajes anteriores para más detalles")
        sys.exit(1)
