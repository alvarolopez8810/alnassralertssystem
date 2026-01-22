# SAFF+ Match Checker

## 📋 Descripción

Esta herramienta permite verificar si hay jugadores destacados en un partido de SAFF+ consultando directamente la API de SAFF+ y comparando con la base de datos de Google Sheets (mreports youth).

## 🚀 Uso

### Ejecutar la aplicación

```bash
streamlit run app_saff_match.py
```

### Cómo funciona

1. **Introduce el URL o ID del partido** de SAFF+
   - URL completa: `https://saffplus.sa/match/ABC123`
   - Solo el ID: `ABC123`

2. **Click en "CHECK MATCH"**
   - El sistema extrae automáticamente los datos del partido desde la API de SAFF+
   - Obtiene todos los jugadores (titulares y suplentes) de ambos equipos

3. **Revisa los resultados**
   - Si hay jugadores destacados en tu base de datos, se mostrarán con toda su información
   - Si no hay coincidencias, recibirás una notificación

## 📁 Archivos creados

### `saff_api.py`
Módulo con funciones para extraer datos de SAFF+ API:
- `extraer_match_id_de_url()`: Extrae el ID del partido desde una URL
- `get_event_details()`: Obtiene detalles del evento desde la API
- `extraer_info_partido()`: Extrae información básica del partido
- `process_lineups()`: Procesa las alineaciones y extrae jugadores
- `obtener_jugadores_partido()`: Función principal que obtiene todos los jugadores
- `formatear_jugadores_para_busqueda()`: Formatea los datos para el sistema de búsqueda

### `app_saff_match.py`
Aplicación Streamlit que:
- Permite introducir URL o ID de partido
- Consulta la API de SAFF+
- Busca coincidencias en Google Sheets
- Muestra jugadores destacados encontrados

## 🔑 Características

- ✅ **Sin necesidad de PDF**: Extrae datos directamente de la API
- ✅ **Búsqueda automática**: Compara con toda la base de datos de Google Sheets
- ✅ **Información completa**: Muestra datos del partido y jugadores
- ✅ **Interfaz intuitiva**: Fácil de usar con Streamlit
- ✅ **Tiempo real**: Consulta datos actualizados de SAFF+

## 📊 Información mostrada

### Del partido:
- Equipos (local y visitante)
- Estadio
- Fecha y hora
- Lineup completo

### De jugadores destacados:
- Nombre, equipo y dorsal
- Posición (genérica y específica)
- Nacionalidad
- Año de nacimiento
- Performance
- Decisión del scout
- Liga
- Hoja de Excel donde está registrado

## 🔗 Ejemplos de URLs válidas

```
https://saffplus.sa/match/V92ZUHBHk21ociydW9xhI
https://saffplus.sa/event/FXSzaQsIp8v0y6aXcRAwf
V92ZUHBHk21ociydW9xhI
FXSzaQsIp8v0y6aXcRAwf
```

## 🛠️ Requisitos

Las dependencias necesarias ya están incluidas en `requirements.txt`:
- `requests==2.31.0` (añadido para llamadas a la API)
- Resto de dependencias existentes del proyecto

## 💡 Ventajas vs sistema PDF

| Característica | Sistema PDF | Sistema SAFF+ API |
|----------------|-------------|-------------------|
| Entrada | Archivo PDF | URL o ID |
| Velocidad | Depende del tamaño del PDF | Rápido (API) |
| Datos | Solo lo que está en el PDF | Datos completos de SAFF+ |
| Actualización | Manual | Tiempo real |
| Facilidad | Requiere descarga | Solo copiar URL |

## 🔐 Configuración

El sistema usa las mismas credenciales de Google Sheets que el sistema principal:
- Variables de entorno (`GCP_*`)
- Streamlit secrets
- Archivo `service_account.json`

No requiere configuración adicional.
