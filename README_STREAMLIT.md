# 🚀 Despliegue en Streamlit Cloud

## 📋 Pasos para Desplegar

### 1. Preparar el Repositorio

Asegúrate de tener estos archivos en tu repositorio:
```
sistema_alertas_jugadores/
├── app.py                      # Aplicación principal
├── pdf_parser.py               # Parser de PDFs
├── buscar_coincidencias.py     # Lógica de búsqueda
├── email_alertas.py            # Sistema de emails
├── config.py                   # Configuración
├── requirements.txt            # Dependencias
├── alnassr_200x200.png         # Logo de Al Nassr
├── mreportsyouth.xlsx          # Base de datos (subir manualmente)
└── .streamlit/
    └── config.toml             # Configuración de tema
```

### 2. Subir a GitHub

```bash
git init
git add .
git commit -m "Initial commit - Al Nassr Alert System"
git branch -M main
git remote add origin https://github.com/tu-usuario/alnassr-alerts.git
git push -u origin main
```

### 3. Desplegar en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona el repositorio
4. Configura:
   - **Main file path**: `app.py`
   - **Python version**: 3.9+

### 4. Configurar Secrets

En Streamlit Cloud, ve a **Settings > Secrets** y añade:

```toml
EMAIL_USER = "alopezmolina4@gmail.com"
EMAIL_PASSWORD = "hsow rbtd fpqr xxjy"
EMAIL_JEFE = "al.scoutinglab@gmail.com"

[EMAIL_DESTINATARIOS]
emails = [
    "al.scoutinglab@gmail.com",
    "rafitagil1975@gmail.com",
    "rafitagil@hotmail.com"
]
```

### 5. Subir Base de Datos

**IMPORTANTE**: El archivo `mreportsyouth.xlsx` debe estar en el mismo directorio que `app.py`.

Opciones:
- **Opción A**: Incluirlo en el repositorio (si es privado)
- **Opción B**: Usar Google Drive o Dropbox con enlace directo
- **Opción C**: Subir manualmente al servidor

## 🧪 Probar Localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📧 Configuración de Email

### Gmail - Contraseña de Aplicación

1. Ve a tu cuenta de Google
2. Seguridad > Verificación en dos pasos (activar)
3. Contraseñas de aplicaciones
4. Genera una nueva contraseña para "Mail"
5. Usa esa contraseña en `EMAIL_PASSWORD`

## 🔒 Seguridad

- ✅ `.env` y `secrets.toml` están en `.gitignore`
- ✅ Nunca subas credenciales al repositorio
- ✅ Usa secrets de Streamlit Cloud para producción
- ✅ El archivo Excel puede contener datos sensibles

## 📱 Uso de la Aplicación

1. **Subir PDF**: Arrastra el archivo de convocatoria
2. **Procesar**: Click en "Process and Send Alerts"
3. **Revisar**: Ver jugadores destacados encontrados
4. **Alertas**: Se envían automáticamente por email

## 🎨 Personalización

### Cambiar Colores

Edita `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#0066CC"  # Azul Al Nassr
backgroundColor = "#FFFFFF"
```

### Cambiar Logo

Reemplaza `alnassr_200x200.png` con tu logo (200x200px recomendado)

## 🐛 Troubleshooting

### Error: "File not found: mreportsyouth.xlsx"
- Asegúrate de que el archivo Excel está en el directorio correcto
- Verifica la ruta en `app.py` línea 134

### Error: "Email not sent"
- Verifica las credenciales en Secrets
- Comprueba que la contraseña de aplicación es correcta
- Revisa que Gmail permite aplicaciones menos seguras

### Error: "PDF parsing failed"
- Verifica que el PDF es del formato MySAFF correcto
- Comprueba que el archivo no está corrupto

## 📊 Monitoreo

Streamlit Cloud proporciona:
- Logs en tiempo real
- Métricas de uso
- Alertas de errores

## 🔄 Actualizar la Aplicación

```bash
git add .
git commit -m "Update: descripción del cambio"
git push
```

Streamlit Cloud se actualizará automáticamente.

## 📞 Soporte

Para problemas técnicos:
- Documentación: [docs.streamlit.io](https://docs.streamlit.io)
- Comunidad: [discuss.streamlit.io](https://discuss.streamlit.io)
