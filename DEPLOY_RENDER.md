# 🚀 Guía de Despliegue en Render

## 📋 Archivos Necesarios para Render

Para desplegar tu aplicación en Render, necesitas subir estos archivos:

### ✅ Archivos Principales (OBLIGATORIOS)

1. **`app_league_checker.py`** - Aplicación principal de Streamlit
2. **`check_league_players.py`** - Lógica de búsqueda de jugadores
3. **`saff_api.py`** - Funciones para interactuar con SAFF+ API
4. **`google_sheets.py`** - Funciones para leer Google Sheets
5. **`buscar_coincidencias.py`** - Lógica de matching de jugadores
6. **`email_resumen_liga.py`** - Funciones para enviar emails
7. **`config.py`** - Configuración de la aplicación
8. **`requirements.txt`** - Dependencias de Python
9. **`render.yaml`** - Configuración de Render (opcional pero recomendado)

### 📁 Carpeta de Configuración

10. **`.streamlit/config.toml`** - Configuración de Streamlit

### 🔐 Archivos de Credenciales (NO SUBIR AL REPOSITORIO)

- **`.env`** - Variables de entorno (configurar en Render)
- **Credenciales de Google** - Configurar como variable de entorno en Render

---

## 🛠️ Pasos para Desplegar en Render

### 1️⃣ Preparar el Repositorio

Si usas Git, asegúrate de tener un `.gitignore`:

```
.env
*.pyc
__pycache__/
.DS_Store
credentials.json
*.pdf
```

### 2️⃣ Crear Servicio en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Click en **"New +"** → **"Web Service"**
4. Conecta tu repositorio de GitHub/GitLab o sube los archivos manualmente

### 3️⃣ Configurar el Servicio

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run app_league_checker.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

**Environment:**
- Python 3.11

### 4️⃣ Configurar Variables de Entorno

En la sección "Environment" de Render, agrega estas variables:

#### Variables de Email
```
EMAIL_USER = tu_email@gmail.com
EMAIL_PASSWORD = tu_contraseña_de_aplicacion
```

#### Credenciales de Google Sheets

Opción A: Como JSON en una sola línea
```
GOOGLE_SHEETS_CREDENTIALS = {"type":"service_account","project_id":"..."}
```

Opción B: Subir archivo de credenciales
- Sube el archivo `credentials.json` como un secreto
- Modifica `google_sheets.py` para leerlo desde la variable de entorno

#### Bearer Token de SAFF+
```
SAFF_BEARER_TOKEN = 5O1SNE9VGH62MA16F2G088VJSV33FLF6
```

### 5️⃣ Modificar `google_sheets.py` para Render

Asegúrate de que `google_sheets.py` pueda leer las credenciales desde variables de entorno:

```python
import os
import json

# Leer credenciales desde variable de entorno
creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
if creds_json:
    creds_dict = json.loads(creds_json)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
else:
    # Fallback a archivo local para desarrollo
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
```

---

## 📦 Lista de Archivos a Subir

### Archivos Python (9 archivos)
- ✅ `app_league_checker.py`
- ✅ `check_league_players.py`
- ✅ `saff_api.py`
- ✅ `google_sheets.py`
- ✅ `buscar_coincidencias.py`
- ✅ `email_resumen_liga.py`
- ✅ `config.py`
- ✅ `requirements.txt`
- ✅ `render.yaml` (opcional)

### Carpeta de Configuración
- ✅ `.streamlit/config.toml`

### NO Subir
- ❌ `.env` (configurar en Render)
- ❌ `credentials.json` (configurar en Render)
- ❌ Archivos PDF
- ❌ `__pycache__/`
- ❌ `.DS_Store`

---

## 🔧 Configuración Específica para Render

### Modificar `config.py`

Asegúrate de que `config.py` lea las variables de entorno:

```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_DESTINATARIOS = ['al.scoutinglab@gmail.com', 'rafitagil@hotmail.com']
```

### Modificar `saff_api.py`

Si el Bearer Token está hardcodeado, cámbialo para usar variable de entorno:

```python
import os

BEARER_TOKEN = os.getenv('SAFF_BEARER_TOKEN', '5O1SNE9VGH62MA16F2G088VJSV33FLF6')
```

---

## 🚨 Problemas Comunes

### Error: "Port already in use"
- Render asigna el puerto automáticamente con `$PORT`
- Asegúrate de usar `--server.port=$PORT` en el start command

### Error: "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que todos los archivos Python estén en el repositorio

### Error: "Google Sheets authentication failed"
- Verifica que la variable `GOOGLE_SHEETS_CREDENTIALS` esté configurada correctamente
- Asegúrate de que sea un JSON válido en una sola línea

### Error: "Email sending failed"
- Verifica que `EMAIL_USER` y `EMAIL_PASSWORD` estén configurados
- Si usas Gmail, necesitas una "contraseña de aplicación", no tu contraseña normal

---

## 📊 Verificar el Despliegue

Una vez desplegado, deberías poder:

1. ✅ Acceder a la aplicación en la URL de Render
2. ✅ Seleccionar una liga y rango de fechas
3. ✅ Ver los jugadores destacados
4. ✅ Descargar el resumen en CSV
5. ✅ Enviar el resumen por email

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en Render (pestaña "Logs")
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que todos los archivos necesarios estén en el repositorio

---

## 📝 Notas Adicionales

- **Plan gratuito de Render**: La aplicación puede tardar ~30 segundos en arrancar después de inactividad
- **Límites**: Render Free tiene 750 horas/mes de uso
- **Actualizaciones**: Cada push a tu repositorio redesplegará automáticamente la aplicación
