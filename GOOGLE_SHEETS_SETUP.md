# 📊 Configuración de Google Sheets

## 🔑 Service Account

Ya tienes una service account configurada:
- **Email**: `alnassrscoutingsystem@hip-sight-474214-k1.iam.gserviceaccount.com`
- **Google Sheet ID**: `1HssweG6CwbKejAb6jACCWu9MtYcqakuePXZYlBhxgxg`

## 🚀 Configuración en Streamlit Cloud

### Paso 1: Obtener las Credenciales JSON

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Selecciona tu proyecto: `hip-sight-474214-k1`
3. Ve a **IAM & Admin** > **Service Accounts**
4. Encuentra: `alnassrscoutingsystem@hip-sight-474214-k1.iam.gserviceaccount.com`
5. Click en los 3 puntos → **Manage keys**
6. **Add Key** > **Create new key** > **JSON**
7. Descarga el archivo JSON

### Paso 2: Configurar en Streamlit Secrets

En Streamlit Cloud, ve a **Settings > Secrets** y añade:

```toml
# Email credentials
EMAIL_USER = "alopezmolina4@gmail.com"
EMAIL_PASSWORD = "hsow rbtd fpqr xxjy"
EMAIL_JEFE = "al.scoutinglab@gmail.com"

# Google Service Account (copia el contenido del JSON aquí)
[gcp_service_account]
type = "service_account"
project_id = "hip-sight-474214-k1"
private_key_id = "TU_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nTU_PRIVATE_KEY_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "alnassrscoutingsystem@hip-sight-474214-k1.iam.gserviceaccount.com"
client_id = "TU_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/alnassrscoutingsystem%40hip-sight-474214-k1.iam.gserviceaccount.com"
```

**IMPORTANTE**: Reemplaza los valores con los de tu archivo JSON descargado.

### Paso 3: Para Testing Local

Crea un archivo `service_account.json` en el directorio del proyecto con el contenido del JSON descargado.

**NO SUBAS ESTE ARCHIVO A GITHUB** (ya está en .gitignore)

## ✅ Verificar Permisos

Asegúrate de que el Google Sheet está compartido con:
```
alnassrscoutingsystem@hip-sight-474214-k1.iam.gserviceaccount.com
```

Con permisos de **Viewer** o **Editor**.

## 🔧 Estructura del Google Sheet

El sistema buscará en todas las pestañas automáticamente. Asegúrate de que cada pestaña tenga estas columnas:

**Columnas requeridas:**
- `Name` - Nombre del jugador
- `Number` - Dorsal
- `Team` - Equipo

**Columnas opcionales (se mostrarán si existen):**
- `Position` - Posición general
- `Spec. Position` - Posición específica
- `Nationality` - Nacionalidad
- `League` - Liga
- `Birth Date` - Fecha de nacimiento
- `Performance` - Nivel de rendimiento
- `Profile Decision` - Decisión del scout
- `Watch` - Estado de seguimiento
- `Scout` - Scout responsable

## 🧪 Testing

Para probar localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app
streamlit run app.py
```

La app se conectará automáticamente a Google Sheets si tienes `service_account.json` en el directorio.
