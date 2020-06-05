import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import math
import base64

"""
Aplicación de Dash para graficar los datos del crecimiento poblacional y la
rersolución de la ecuación diferencial logistica
:author: Pablo Sao
:date: 04 de junio de 2020
"""

def calculo_ecuacion(cantidad_datos):
    valores = []
    for generar in range(cantidad_datos):
        p = (0.005552309*331323.9645)/( (0.000000346*331323.9645) + math.exp(-0.005552309*generar)  )
        valores.append(p)

    return valores



def generaGrafica():

    # Obteniendo los datos

    DATA = pd.read_excel('data.xlsx', sheet_name='Datos')

    cLayout = go.Layout(title='Población Mundial',
                        # Same x and first y
                        xaxis_title='Fecha',
                        yaxis_title='Personas (en millones)',
                        height=500
                        )
    P = calculo_ecuacion(len(DATA.index))

    trace1 = go.Scatter(x=DATA['Año'], y=DATA['Inicial'], name='Población Valores Defecto')
    trace2 = go.Scatter(x=DATA['Año'], y=DATA['Inicial sin NRR'], name='Población Valores Defecto (sin NRR)')

    trace4 = go.Scatter(x=DATA['Año'], y=P, name='Población Ecuación Diferencial')

    return dcc.Graph(id='graph', figure={
                'data': [trace1,trace2,trace4],
                'layout': cLayout
            })



DES_ECUACION_LOGISTICA = \
"""
Zill (2019), indica que aproximadamente en 1840 el matemático y biólogo P. Verhulst 
investigó modelos matemáticos para predecir la población humana en varios países, 
donde las curvas logísticas predicen con bastante exactitud el crecimiento de ciertos 
tipos de bacterias, protozoarios, pulgas de agua y moscas de frutas en ambientes limitados. 
Siendo la ecuación:
"""

image_filename = 'ecuacion_logistica.png' # replace with your own image
ECUACION_LOGISTICA = base64.b64encode(open(image_filename, 'rb').read())



# Link Repositorio
LINK_GITHUB = 'https://github.com/psao/UVG-MM2021-Crecimiento-Poblacional'



# Iniciando la aplicacion
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Creando aplicacion de Dash
app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.UNITED]
)
server = app.server
#Colocando titulo a la pestania
app.title = 'Población Mundial'


#Layout de la pagina
app.layout = html.Div(children=[
    dbc.Row(
            dbc.Col(
                (
                    html.H1(children='Población Mundial'),
                    html.H4(children='Pablo Sao & Shirley Marroquín'),
                    html.Br(),
                    html.A('Código en Github', href=LINK_GITHUB),
                    html.Br(),
                ),
                width={"size": 6, "offset": 1},
            )
    ),

    dbc.Row(
        [
            dbc.Col((
                dbc.Tabs([

                    # Grafica
                    dbc.Tab((
                        dbc.CardBody(
                            dbc.CardBody([
                                html.Div(
                                    generaGrafica()
                                ),
                            ]),
                            className='mt-3'
                        )
                    ),label="Gráficas Población Mundial",disabled=False),

                    # Informacion
                    dbc.Tab((

                            dbc.CardBody(
                                dbc.CardBody([
                                    html.H2(children='Ecuación Logística'),
                                    html.P(DES_ECUACION_LOGISTICA),

                                    html.Div([
                                        html.Img(src='data:image/png;base64,{}'.format(ECUACION_LOGISTICA.decode()))
                                    ], style={'textAlign': 'center'}),

                                ]),
                                className='mt-3'
                            )

                        ),label="Información",disabled=False),
                    ]),
            ),
            width={"size": 10, "offset": 1}),
        ]
    ),






])

if __name__ == '__main__':
    app.run_server()
