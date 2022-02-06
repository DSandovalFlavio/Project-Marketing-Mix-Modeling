# Desarrorllo de Marketing Mix Model (MMM)
# Autor: @dsandovalflavio
# Framework: streamlit

#  Importacion de librerias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

def cargar_datos():
    """
    Funcion para cargar los datos de la base de datos
    """
    # Cargar datos de la base de datos
    
    path_archivos = "./Data/"
    data_CF = pd.read_csv(path_archivos + "mmm.csv")
    return data_CF

def main():
    # Titulo de la aplicacion
    st.title("Marketing Mix Model (MMM)")
    st.markdown("""By [@DSandovalFlavio](https://github.com/DSandovalFlavio) and
                      [@Chesar832](https://github.com/Chesar832)""")
    # Descripcion de la aplicacion
    st.markdown("""
                ## Problema
                En el Marketing uno de los mayores problemas es la atribución. 
                Dado que los clientes reciben múltiples impactos online y offline, 
                no siempre es fácil saber qué canales ofrecen mejores resultados.

                ### *"La mitad del dinero que me gasto en publicidad es un desperdicio: el problema es que no sé qué mitad es"*
                John Wanamaker

                ## ¿Ques es el Marketing Mix Model (MMM)?
                El marketing mix modeling es un tipo de modelado que permite conocer 
                la relación entre cada canal de marketing en los que se invierte dentro 
                de una empresa y sus respectivos resultados (ventas)

                ### Utilidad del modelo
                Este modelado es útil porque hace visible los rendimientos con respecto a 
                inversión y ventas por canal. Además, permite predecir escenarios futuros y 
                el comportamiento del ROI.

                **Que se obtiene con el modelado?**
                
                Se espera obtener curvas de saturación por cada canal disponible en el 
                conjunto de datos elegido, para conocer qué tipo de patrón de inversión es el más 
                adecuado para la empresa en cuestión.

                ---

                ## Implementación

                ### Datos

                """)
    # Mostrar la data en streamlit
    data = cargar_datos()
    st.write(data)
    st.markdown("""A continuación se decriben las variables contenidas en el dataset.""")
    st.markdown("""
                | **VARIABLE** |                **DESCRIPCIÓN**                      |
                | :------------|----------------------------------------------------:| 
                | Date         | Fecha en la que se realizó la inversión             |
                | OpenTV       | Presupuesto de promoción televisiva abierta.        |
                | PayTV        | Presupuesto de promoción televisiva de paga.        |
                | Radio        | Presupuesto de promoción radiofónica                |
                | Print        | Presupuesto de promoción en medios impresos         |
                | Facebook     | Presupuesto de promoción en Facebook                |
                | Google       | Presupuesto de promoción en Google                  |
                | Email        | Presupuesto de promoción en correos publicitarios   |
                | Sales        | Ventas obtenidas                                    |
                """)
    st.markdown("""
                ---
                #### Como a inviertido la marca a lo largo de los años?
                
                """)
    # Data para graficar
    data_CF = data.copy()
    data_CF['Date'] = pd.to_datetime(data_CF['Date'])
    data_CF['year_month'] = data_CF['Date'].dt.strftime('%Y-%m')
    data_CF['Mes_No'] = data_CF['Date'].dt.month
    # Mes en texto
    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    data_CF['Mes'] = data_CF['Mes_No'].map(meses)
    data_CF['Año'] = data_CF['Date'].dt.year
    data_CF['Año'] = data_CF['Año'].astype(str)
    data_CF['Inversion Total'] = data_CF[['Print', 'Email', 'Radio', 'Facebook', 'Google', 'PayTV', 'OpenTV']].sum(axis=1)

    # Grafico de pie
    pie_year = px.pie(data_CF, 
                    values='Inversion Total',  
                    names='Año', 
                    title='Inversion por año')
    st.plotly_chart(pie_year)
    st.markdown("""Se observa que la inversión en los años 2018 y 2020 fue la mayor, 
                con una inversión de $1.8 millones de pesos.""")

    # Comportamiento de la inversion por mes a lo largo de los años
    com_inv_mes = px.bar(data_CF.groupby(['Año', 'Mes_No', 'Mes'])['Inversion Total'].sum().reset_index(), 
                        x="Mes", 
                        y="Inversion Total", 
                        color="Año",
                        text="Inversion Total")
    com_inv_mes.update_traces(texttemplate='%{text:.2s}')
    st.plotly_chart(com_inv_mes)

    # Grafico de pie con radio button para elegir el año
    # crear una lista con los años para streamlit
    lista_anios = data_CF['Año'].unique()
    opcion_anio = st.selectbox('Seleccione el año', lista_anios)
    # grafico de pie para el año seleccionado
    pie_anio = px.pie(pd.melt( data_CF.query('Año == @opcion_anio'),
                                id_vars=['Date'], 
                                value_vars=['Print', 'Email', 'Radio', 'Facebook', 'Google', 'PayTV', 'OpenTV'],
                                var_name= "Medio",
                                value_name= "Inversion"),
                    values='Inversion', 
                    names='Medio',
                    title='Share of Investment by Media')
    st.plotly_chart(pie_anio)



    # graficar la data en streamlit
    df = data[['Sales','Print', 'Email', 'Radio', 'Facebook', 'Google', 'PayTV', 'OpenTV']].corr().round(2)
    fig = ff.create_annotated_heatmap( df.values.tolist(),
                                        x=df.columns.values.tolist(),
                                        y=df.index.values.tolist(),
                                        colorscale='Viridis')
    fig.update_layout(title_text='Correlacion')
    fig['data'][0]['showscale'] = True
    st.plotly_chart(fig)
    

if __name__ == '__main__':
    main()
