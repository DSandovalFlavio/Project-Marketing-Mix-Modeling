# Desarrorllo de Marketing Mix Model (MMM)
# Autor: @dsandovalflavio
# Framework: streamlit

#  Importacion de librerias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def cargar_datos():
    """
    Funcion para cargar los datos de la base de datos
    """
    # Cargar datos de la base de datos
    
    path_archivos = "./Data/"
    InversionMedia = pd.read_csv(path_archivos + "InversionMedia.csv")
    Sales = pd.read_csv(path_archivos + "Sales.csv")
    data_CF = pd.merge(InversionMedia, Sales, on="Date", how="left").rename(columns={"Pay TV": "PayTV", "Open TV": "OpenTV"})
    return data_CF

def main():
    # Titulo de la aplicacion
    st.title("Marketing Mix Model (MMM)")
    st.markdown("""by @dsandovalflavio""")
    # Descripcion de la aplicacion
    st.markdown("""
                ## Descripcion
                En este proyecto se realiza paso a paso un marketing mix modeling 
                que tiene como objetivo obtener las contribuciones de cada uno de los canales 
                de marketing(Inversion) en las ventas de una empresa, y de esta manera 
                poder hacer optimizaciones.
                """)
    # Mostrar primeras 5 filas de la data en streamlit
    data = cargar_datos()
    st.write(data.head())
    # graficar la data en streamlit
    plot = px.histogram(data, x=['OpenTV','PayTV','Radio'],
            marginal="box",
            title="Histograma de " + 'Medios Off')
    st.plotly_chart(plot)
    

if __name__ == '__main__':
    main()
