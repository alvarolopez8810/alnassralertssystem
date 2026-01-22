from sistema_alertas_completo import procesar_acta_y_enviar_alertas

pdf_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/Acta2AlNassr.pdf'
excel_path = '/Users/alvarolopezmolina/Desktop/alertasalnassr/mreportsyouth.xlsx'

print("Iniciando prueba del sistema de alertas...")
print(f"PDF: {pdf_path}")
print(f"Excel: {excel_path}\n")

jugadores = procesar_acta_y_enviar_alertas(pdf_path, excel_path)

if jugadores:
    print("\n" + "="*80)
    print("RESUMEN DE JUGADORES ENCONTRADOS:")
    print("="*80)
    for j in jugadores:
        print(f"\n{j['Nombre']} (#{j['Dorsal']}) - {j['Equipo']}")
        print(f"  Posición: {j['Posicion']} | Tipo: {j['Tipo']}")
        print(f"  Decisión: {j['Decisión']}")
        print(f"  Performance: {j['Performance']}")
        print(f"  Scout: {j['Scout']}")
        print(f"  Pestaña Excel: {j['Pestaña_Excel']}")
