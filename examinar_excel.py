import pandas as pd
import sys

excel_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/mreportsyouth.xlsx'

try:
    xls = pd.ExcelFile(excel_path)
    print(f"Pestañas encontradas: {xls.sheet_names}\n")
    
    for sheet in xls.sheet_names:
        print(f"\n{'='*80}")
        print(f"PESTAÑA: {sheet}")
        print('='*80)
        df = pd.read_excel(excel_path, sheet_name=sheet)
        print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"\nColumnas: {list(df.columns)}")
        print(f"\nPrimeras 3 filas:")
        print(df.head(3))
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
