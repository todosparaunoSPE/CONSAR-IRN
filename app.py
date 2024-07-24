# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:54:19 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Título principal de la aplicación
st.title("CONSAR: Indicador de Rendimiento Neto (IRN)")

# Agregar sección de Ayuda en el sidebar
st.sidebar.title("Ayuda")
st.sidebar.info(
    "Esta aplicación muestra un análisis del Indicador de Rendimiento Neto (IRN) a partir de un archivo XLSX predefinido. "
    "Selecciona los filtros para cada hoja de datos y observa los resultados en forma de tabla y gráfico de barras."
)

# Cargar el archivo XLSX directamente
file_path = 'IRN-ene 2021-mayo-2024.xlsx'

# Obtener los nombres de las hojas del archivo XLSX
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Verificar nombres de hojas
expected_sheets = ['IRN', 'IRN_promedio', 'IRN_ponderado']

for sheet in expected_sheets:
    if sheet not in sheet_names:
        st.error(f"La hoja '{sheet}' no se encontró en el archivo XLSX cargado.")
        st.stop()

# Leer las hojas del archivo XLSX
df1 = pd.read_excel(file_path, sheet_name='IRN')
df2 = pd.read_excel(file_path, sheet_name='IRN_promedio')
df3 = pd.read_excel(file_path, sheet_name='IRN_ponderado')

# Función para mostrar filtros y gráficos para cada dataframe
def display_dataframe(df, filters, title):
    st.write(f"### {title}")

    # Aplicar filtros
    for i, col in enumerate(filters):
        unique_vals = df[col].unique()
        default_vals = list(unique_vals) if len(unique_vals) > 0 else []  # Convertir a lista si hay valores únicos

        # Generar una clave única para cada multiselect
        widget_key = f"{title}_filter_{i}"

        selected_vals = st.multiselect(f"Filtrar por {col}", unique_vals, default=default_vals, key=widget_key)

        df = df[df[col].isin(selected_vals)]

    # Mostrar dataframe filtrado
    st.dataframe(df)

    # Crear gráfico de barras si hay datos filtrados
    if not df.empty:
        # Convertir columnas relevantes a tipo numérico si es necesario
        numeric_columns = df.select_dtypes(include=['float', 'int']).columns.tolist()

        if numeric_columns:
            # Convertir fechas a cadenas antes de usarlas en el título del gráfico
            selected_dates_str = [str(date) for date in selected_vals]
            date_filters = ", ".join(selected_dates_str)

            # Construir el título del gráfico con las fechas seleccionadas
            fig_title = f"{title} - Fechas: {date_filters}"

            fig = px.bar(df, x=filters[0], y=numeric_columns, barmode='group', title=fig_title)
            st.plotly_chart(fig)
        else:
            st.warning("No se encontraron columnas numéricas para crear el gráfico.")
    else:
        st.info("No hay datos disponibles para mostrar con los filtros seleccionados.")

# Mostrar filtros y gráficos para cada hoja
display_dataframe(df1, ['AFORE', 'SIEFORE', 'Fecha'], "IRN-Ene 2021-May 2024")
display_dataframe(df2, ['AFORE', 'SIEFORE', 'Fecha'], "IRN_promedio")
display_dataframe(df3, ['AFORE', 'Fecha'], "IRN_ponderado")

# Aviso de derechos de autor
#st.sidebar.markdown("""
#    ---
#    © 2024. Todos los derechos reservados.
#    Creado por jahoperi.
#""")

# Pie de página en la barra lateral
st.sidebar.write("© 2024 Todos los derechos reservados")
st.sidebar.write("© 2024 Creado por: Javier Horacio Pérez Ricárdez")
st.sidebar.write("PensionISSSTE: Analista UEAP B")
