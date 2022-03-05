# Desarrorllo de Marketing Mix Model (MMM)
# Autor: @dsandovalflavio
# Framework: streamlit

#  Importacion de librerias
from tkinter import Y
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    st.markdown("""
                ### Analisis Exploratorio
                A continuación se decriben las variables contenidas en el dataset.""")
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
                    names='Año')
    st.plotly_chart(pie_year)
    st.markdown("""Se observa que la inversión en los años 2018 y 2020 fueron las mas altas.""")

    # Comportamiento de la inversion por mes a lo largo de los años
    com_inv_mes = px.bar(data_CF.groupby(['Año', 'Mes_No', 'Mes'])['Inversion Total'].sum().reset_index(), 
                        x="Mes", 
                        y="Inversion Total", 
                        color="Año",
                        text="Inversion Total")
    com_inv_mes.update_traces(texttemplate='%{text:.2s}')
    st.plotly_chart(com_inv_mes)
    st.markdown("""
                - Se observa que la inversión en los meses de Junio y Octubre fueron las mas altas
                - En Junio se hace hizo la mayor inversion 2020 y 2019 
                - Abril y Mayo del 2019 y 2018 fueron muy parecidas inversion
                - Noviembre normalmente baja la inversion para subir en Diciembre
                """)

    st.markdown("""
                #### Como se distribuye la inversion en cada medio a lo largo de los años?
                """)
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
                    names='Medio')
    st.plotly_chart(pie_anio)
    inv_año = { '2018': '''
                        - El 75% de la inversión fue en los medios OpenTV, PayTV, Google y Radio
                        - El 25% de la inversión fue en los medios impresos, email y Facebook''', 
                '2019': '''
                        - El 69% de la inversión fue en los medios OpenTV, PayTV, Google y Radio
                        - El 31% de la inversión fue en los medios impresos, email y Facebook''', 
                '2020': '''
                        - El 76% de la inversión fue en los medios OpenTV, PayTV, Google y Radio
                        - El 24% de la inversión fue en los medios impresos, email y Facebook''', 
                '2021': '''
                        - El 77% de la inversión fue en los medios OpenTV, PayTV, Google y Radio
                        - El 23% de la inversión fue en los medios impresos, email y Facebook'''}
    st.markdown(inv_año[opcion_anio])
    
    st.markdown("""#### Como se distribuye generalmente la inversión en los medios""")
    list_metrics = ['mean', 'std', 'max', 'cv']
    opcion_metric = st.selectbox('Ordenar por: ', list_metrics)
    # Comportamiento de la inversion en medios a total
    data_inv_medio = data_CF[[ 'Print', 'Email', 'Radio', 
                                'Facebook', 'Google', 'PayTV', 
                                'OpenTV']].describe().round(2).T
    data_inv_medio['cv'] = (data_inv_medio['std'] / data_inv_medio['mean']).round(3)
    data_inv_medio = data_inv_medio[list_metrics].sort_values(by=opcion_metric, ascending=True)
    heat_dist = ff.create_annotated_heatmap( data_inv_medio.values.tolist(),
                                        x=data_inv_medio.columns.values.tolist(),
                                        y=data_inv_medio.index.values.tolist(),
                                        colorscale='Viridis')
    st.plotly_chart(heat_dist)
    
    st.markdown("""
                - La mayor inversion se llevo acabo en OpenTV, con una inversion de 18,164.39
                - La menor inversion se llevo acabo en Email, con una inversion de 873.80
                - Google y Radio tienen una distribucion de inversiones muy similar 
                - La inversion en los medios como PayTV, Open TV y Facebook son muy similares
                - En promedio seinvierten por lo menos 1000 pesos en los medios Facebook, Print, Email
                - En promedio un poco mas de 3000 dolares en medios paytv opentv radio google
                """)
    
    medios = ['Print', 'Email', 'Radio', 'Facebook', 'Google', 'PayTV', 'OpenTV']
    opcion_metric = st.selectbox('Selecciona un medio: ', medios)
    scatter_medio = go.Figure(data=[go.Scatter(x=data_CF['Date'], y=data_CF[opcion_metric], name=opcion_metric)])
    scatter_medio.update_layout(width=800, height=300)
    st.plotly_chart(scatter_medio)
    st.markdown("""podemos ver que print y email mantienen sus inversiones por mas numero de semanas,
                    mientras que los demas medios tienden a prender y apagar inversiones cada semana""")
    
    # Como afecta la inversion total de medios en las ventas
    st.markdown("""#### Como afecta la inversion total de medios en las ventas? """)
    
    data_CF['year_month'] = data_CF['Date'].dt.strftime('%Y-%m')
    data_CF['InversionTotal'] = data_CF[['Print', 'Email', 'Radio', 'Facebook', 'Google', 'PayTV', 'OpenTV']].sum(axis=1)
    data_tem = data_CF.groupby(['year_month'], as_index = False )['InversionTotal', 'Sales'].sum()

    inv_ventas = make_subplots(specs=[[{"secondary_y": True}]])
    inv_ventas.add_trace(go.Bar(x=data_tem['year_month'], 
                        y=data_tem['Sales'], 
                        marker_color='LightSkyBlue',
                        name='Sales'), secondary_y=False)
    inv_ventas.add_trace(go.Scatter(x=data_tem['year_month'], 
                            y=data_tem['InversionTotal'],
                            marker_color='MediumPurple',
                            name='InversionTotal'), secondary_y=True)
    inv_ventas.update_layout(
                        xaxis_title='Date', 
                        yaxis_title='Inversion Total', 
                        barmode='group')
    inv_ventas.update_layout(width=800, height=500)
    st.plotly_chart(inv_ventas)
    st.markdown('Las ventas responden positivamente a la inversion total de medios')
    st.markdown('#### Como se correlacionan las ventas con la inversion en cada medio')
    # graficar la data en streamlit
    df = data[['Sales','Print', 'Email', 
            'Radio', 'Facebook', 'Google', 
            'PayTV', 'OpenTV']].corr()[['Sales']].round(2).sort_values(by='Sales', 
                                                                        ascending=True)
    corr = ff.create_annotated_heatmap( df.values.tolist(),
                                        x=df.columns.values.tolist(),
                                        y=df.index.values.tolist(),
                                        colorscale='Viridis')
    st.plotly_chart(corr)
    
    st.markdown("""Google tiene la mayor correlacion con las ventas,
                Email aun que no es donde mas se invierte tiene un buen coeficiente,
                PayTV por el contrario se invierte mucho y no tiene un coeficiente tan bueno como los demas medios""")
    st.markdown("""
                ### Modeling
                El objetivo de este modelo es obtener la atribucion de cada medio a las ventas,
                y para obtener estos valores se utilizara como base una regresion lineal multiple, añadiendo 
                ingenieria de caracteristicas propias de marketing como lo son:
                
                - **Efectos de Arrastre**: Con esto se modela el impacto de la inversion en las semanas siguientes
                    a la inversion mediante un efecto de degradacion semana a semana, estos parametros de cuantas semanas y con que fuerza
                    dura la degradacion sera optimizado en el proceso de modeling, para obtener el mejor parametro para cada medio.
                - **Efecto de Saturacion**: Con esto se modela como es que el medio se satura, es decir, cuando se invierten los primeros 10000 pesos
                    tiene un mayor efecto, que cuando de invierten 5000 pesos mas estos ya no generan la mitad de los beneficios que generaron los primeros 10000,
                    para generar este efecto se aplican funciones no lineales, como la exponencial o en este caso Adbudg.
                
                **Regresion Lineal Multiple** se utilizara con las variables que ya cuentan con las tranformaciones,
                para obtener los coeficientes de la atribucion de cada medio a las ventas.
                
                **ROI**: con los valores de ventas por medio y la inversion de cada medio podemos obtener el retorno de inversion, 
                es decir, el beneficio que se obtiene de la inversion de cada medio.
                
                Por ultimo graficaremos las curvas de retorno de inversion para cada medio, y el ROI para obtener los mejores montos de inversion.
        """)
    st.image('./Resources/Pipeline.png', width=800)
    
    # Data con Features Engineering
    st.markdown("""#### Como cambia la correlacion entre las ventas y la inversion de cada medio con la implementacion de Features Engineering""")
    data_FE_raw = pd.read_csv('./DataSaturada.csv').set_index('Date')
    data_FE = data_FE_raw[['Sales','OpenTV_sat', 'PayTV_sat', 'Radio_sat', 'Print_sat', 'Facebook_sat', 'Google_sat', 'Email_sat']]
    data_FE = data_FE.corr()[['Sales']].round(2).sort_values(by='Sales', 
                                                            ascending=True)
    corr_FE = ff.create_annotated_heatmap( data_FE.values.tolist(),
                                    x=data_FE.columns.values.tolist(),
                                    y=data_FE.index.values.tolist(),
                                    colorscale='Viridis')
    st.plotly_chart(corr_FE)
    
    st.markdown("""#### Que tan saturados se encuentran los medios?""")
    # Curvas de saturacion
    medios2 = ['Email', 'Radio', 'Facebook', 'Google', 'PayTV', 'OpenTV', 'Print']
    medio = st.selectbox('Selecciona un medio: ', medios2)
    medio_sat = medio+'_sat'
    data_adstock = data_FE_raw[data_FE_raw[medio_sat] != 0]
    curvas_sat = px.scatter(data_adstock,
                            x = medio, 
                            y = medio_sat)
    st.plotly_chart(curvas_sat)
    des_curvas = { 'Email' : 'Email aun no esta saturado, es decir, se podria invertir un poco mas para obtener una mejor atribucion', 
                    'Radio' : 'Radio aun no esta saturado, se ve un crecimiento mas lineal, se podria invertir mas para obtener una mejor atribucion', 
                    'Facebook' : 'Facebook ya esta saturado, se tendria que analizar si la marca solo esta decidiendo tener precencia en el medio',
                    'Google' : 'Google ya esta saturado, se tendria que analizar si la marca solo esta decidiendo tener precencia en el medio', 
                    'PayTV': 'PayTV ya esta saturado, se tendria que analizar si la marca solo esta decidiendo tener precencia en el medio',  
                    'OpenTV' : 'OpenTV aun no esta saturado, se ve un crecimiento mas lineal, se podria invertir mas para obtener una mejor atribucion', 
                    'Print' : 'Print aun no esta saturado, es decir, se podria invertir un poco mas para obtener una mejor atribucion'}
    st.markdown(des_curvas[medio])
    
    st.markdown("""#### ROI - Retorno de inversion""")
    # ROI
    atribucion_ventas_medio = pd.read_csv('./adj_contributions.csv')
    atribucion_ventas_medio['Date'] = pd.to_datetime(atribucion_ventas_medio['Date'])
    atribucion_ventas_medio = atribucion_ventas_medio.set_index('Date')
    atribucion_ventas_medio = atribucion_ventas_medio.rename(columns=lambda x: x+'_revenue')
    atribucion_ventas_medio = atribucion_ventas_medio.drop(columns=['Base_revenue'])
    
    investment_medio = pd.read_csv('./Data/mmm.csv')
    investment_medio['Date'] = pd.to_datetime(investment_medio['Date'])
    investment_medio = investment_medio.set_index('Date')
    investment_medio = investment_medio.rename(columns=lambda x: x+'_investment')
    investment_medio = investment_medio.drop(columns=['Sales_investment'])
    
    # calcular el ROI para cada medio
    atribucion_investment_medio = pd.merge(investment_medio, atribucion_ventas_medio, how='inner', left_index=True, right_index=True)
    amedios3 = ['OpenTV', 'Print', 'Email', 'Radio', 'Facebook', 'Google', 'PayTV']
    for medio in amedios3:
        atribucion_investment_medio[medio+'_ROI'] = (atribucion_investment_medio[medio+'_revenue'] - atribucion_investment_medio[medio+'_investment'])/atribucion_investment_medio[medio+'_investment']
    
    amedios4 = ['OpenTV', 'Print', 'Facebook', 'Google', 'PayTV', 'Email', 'Radio']
    medio_select = st.selectbox('Selecciona un medio: ', amedios4)
    atribucion_investment_medio = atribucion_investment_medio[atribucion_investment_medio[medio_select+'_investment'] != 0]
    roi_plot = make_subplots(specs=[[{"secondary_y": True}]])
    # revenue vs investment
    roi_plot.add_trace(go.Scatter(  x=atribucion_investment_medio[medio_select+'_investment'],
                                    y=atribucion_investment_medio[medio_select+'_revenue'],
                                    mode='markers',
                                    name='Revenue vs Investment'),
                        secondary_y=False)
    # revenue vs ROI
    roi_plot.add_trace(go.Scatter(  x=atribucion_investment_medio[medio_select+'_investment'],
                                    y=atribucion_investment_medio[medio_select+'_ROI'],
                                    mode='markers',
                                    name='Revenue vs ROI'),
                        secondary_y=True)
    roi_plot.update_layout( #title_text=medio_select+' ROI',
                            yaxis_title='Revenue',
                            yaxis2_title='ROI',
                            xaxis_title='Investment')
    st.plotly_chart(roi_plot)

if __name__ == '__main__':
    main()
    

