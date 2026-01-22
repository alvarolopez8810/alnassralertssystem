# Sistema de Alertas de Jugadores - Al Nassr FC

Sistema automático que:
1. **Parsea PDFs** de actas de partido (convocatorias)
2. **Busca coincidencias** con jugadores destacados en la base de datos Excel
3. **Envía alertas automáticas** por email cuando encuentra jugadores destacados convocados

## 📋 Requisitos

- Python 3.7+
- Cuenta de Gmail con contraseña de aplicación configurada
- Archivo `mreportsyouth.xlsx` con base de datos de scouting

## 🚀 Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar credenciales en el archivo `.env` (ya creado)

## 🎯 Uso Principal - Sistema Completo

### Procesar un acta de partido:

```bash
python3 sistema_alertas_completo.py /ruta/al/acta.pdf
```

**Ejemplo:**
```bash
python3 sistema_alertas_completo.py /Users/alvarolopezmolina/Desktop/alertasalnassr/Acta2AlNassr.pdf
```

El sistema automáticamente:
- ✅ Extrae todos los jugadores del PDF
- ✅ Busca coincidencias en todas las pestañas del Excel
- ✅ Envía un email por cada jugador destacado encontrado

### Probar con el script de prueba:

```bash
python3 test_sistema.py
```

## 📦 Módulos del Sistema

### 1. `pdf_parser.py`
Extrae información de jugadores desde PDFs de actas de partido.

```python
from pdf_parser import extraer_jugadores_pdf, extraer_info_partido

df_jugadores = extraer_jugadores_pdf('acta.pdf')
info_partido = extraer_info_partido('acta.pdf')
```

### 2. `buscar_coincidencias.py`
Busca jugadores del PDF en la base de datos Excel.

```python
from buscar_coincidencias import buscar_coincidencias_en_todas_pestanas

jugadores_encontrados = buscar_coincidencias_en_todas_pestanas(
    df_jugadores, 
    'mreportsyouth.xlsx'
)
```

### 3. `email_alertas.py`
Envía alertas por email.

```python
from email_alertas import enviar_alerta_jugador

jugador_info = {
    'Nombre': 'Mohammed Al-Salem',
    'Equipo': 'Al Nassr FC',
    'Dorsal': 7,
    'Decisión': 'SEGUIR',
    'Posicion': 'MF',
    'Tipo': 'Titular',
    'Performance': 'Excelente',
    'Watch': 'Yes',
    'Scout': 'Alvaro Lopez',
    'Año_Nacimiento': 2008,
    'Partido': '#138 - Thursday 15 January'
}

enviar_alerta_jugador(jugador_info)
```

## 🔍 Criterios de Búsqueda

El sistema busca coincidencias usando:
- **Dorsal (Number)**: Coincidencia exacta
- **Nombre (Name)**: Similitud > 85% (normalizado)
- **Equipo (Team)**: Coincidencia parcial (Al-Nassr, Al Nassr FC, etc.)

## 📧 Formato de Alertas

Cada email incluye:
- Nombre del jugador
- Equipo y dorsal
- Posición y tipo (Titular/Suplente)
- Año de nacimiento
- **Decisión Scout** (SEGUIR, FICHAR, etc.)
- Performance y Watch status
- Scout responsable
- Información del partido

## 🧪 Probar Solo el Email

```bash
python3 email_alertas.py
```

## 📁 Estructura de Archivos

```
sistema_alertas_jugadores/
├── .env                          # Credenciales (NO subir a Git)
├── .gitignore                    # Protege archivos sensibles
├── config.py                     # Carga variables de entorno
├── pdf_parser.py                 # Parser de PDFs
├── buscar_coincidencias.py       # Lógica de búsqueda
├── email_alertas.py              # Sistema de emails
├── sistema_alertas_completo.py   # Script principal
├── test_sistema.py               # Script de prueba
├── requirements.txt              # Dependencias
└── README.md                     # Este archivo
```

## 🔒 Seguridad

- El archivo `.env` contiene credenciales sensibles
- Está incluido en `.gitignore` para no subirlo a repositorios
- Nunca compartas tu contraseña de aplicación de Gmail

## 💡 Ejemplo de Flujo Completo

```bash
# 1. Descargar acta de partido (PDF)
# 2. Ejecutar el sistema
python3 sistema_alertas_completo.py ~/Downloads/acta_partido.pdf

# 3. El sistema automáticamente:
#    - Parsea el PDF
#    - Busca en mreportsyouth.xlsx
#    - Envía emails a al.scoutinglab@gmail.com
```
