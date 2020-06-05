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

def getConstanteA(valor_inicial,observacion_1,observacion_2):
    constante_a = (1/10) * math.log( ( ( (valor_inicial**2) * observacion_2) - observacion_2  ) / ( ( (valor_inicial**2) * observacion_1) - observacion_1  ) )
    return  constante_a

def getConstanteB(valor_inicial,observacion_1,constante_a):
    constante_b = (constante_a * ( (observacion_1 * math.exp(-10*constante_a)) - valor_inicial) )/(observacion_1*valor_inicial*(math.exp(-10*constante_a) - 1))
    return constante_b

def getConstanteC2(valor_inicial,constante_a,constante_b):
    constante_c2 = valor_inicial / (constante_a - (valor_inicial*constante_b))
    return constante_c2

def calculo_ecuacion(cantidad_datos):
    valores = []
    for generar in range(cantidad_datos):
        p = int(round( (0.005552309*331323.9645)/( (0.000000346*331323.9645) + math.exp(-0.005552309*generar)) ))
        valores.append(p)

    return valores

def getcalculo_ecuacion(cantidad_datos,constante_a,constante_b,constante_c2):
    valores = []
    for generar in range(cantidad_datos):
        p = int(round( (constante_a * constante_c2)/( (constante_b * constante_c2) + math.exp(-constante_a * generar)) ))
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

    trace1 = go.Scatter(x=DATA['Año'], y=DATA['Datos por Defecto'], name='Población Valores Defecto')
    trace2 = go.Scatter(x=DATA['Año'], y=DATA['Datos por Defecto sin NRR'], name='Población Valores Defecto (sin NRR)')

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

ECUACION_LOGISTICA = "\[ { dP \over dt} = P(a - bP) \]"
ECUACION_LOGISTICA_RESOLUCION = "\[ P(t) = { aC_2 \over bC_2 + e^{-at}} \]"
# Link Repositorio
LINK_GITHUB = 'https://github.com/psao/UVG-MM2021-Crecimiento-Poblacional'

# leyendo datos de Excel
DATOS = pd.read_excel('data.xlsx', sheet_name='Datos')

# Obteniendo nombre de las columnas
OPCIONES = list(DATOS.columns)
OPCIONES.remove('Año')


#valor_inicial = DATOS.iloc[0]['Datos por Defecto']
#valor_1 = DATOS.iloc[10]['Datos por Defecto']
#valor_2 = DATOS.iloc[20]['Datos por Defecto']

#con_a = getConstanteA(valor_inicial,valor_1,valor_2)
#con_b = getConstanteB(valor_inicial,valor_1,con_a)
#print(getConstanteC2(valor_inicial,con_a,con_b))

# Creando aplicacion de Dash
app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.UNITED],
    external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML',],
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

                                dbc.Row([
                                    dbc.Col(
                                        html.Div(children='''Datos Disponibles:'''),
                                    ),
                                    dbc.Col(
                                        html.Div(children='''Ecuación:'''),
                                    ),
                                ]),
                                dbc.Row([
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='select_column',
                                            options=[
                                                {'label': i, 'value': i } for i in OPCIONES
                                            ],
                                            multi=False,
                                            value=OPCIONES[0],
                                            placeholder='Seleccion de Datos para Ecuación',
                                        )
                                    ),
                                    dbc.Col(
                                        html.Div(id='formula_generada'),
                                    ),
                                ],),

                                html.Br(),
                                html.Div(id='grafica_pronostico'),
                            ]),
                            className='mt-3'
                        )
                    ),label="Gráficas Población Mundial",disabled=False),

                    # Informacion
                    dbc.Tab((

                            dbc.CardBody(
                                dbc.CardBody([
                                    html.H2(children='Ecuación Logística'),
                                    html.P(DES_ECUACION_LOGISTICA, style={'textAlign': 'justify'}),
                                    html.P(children=[ECUACION_LOGISTICA], style={'textAlign': 'center'}),
                                    html.P(
                                    """
                                    Primero se determinó la ecuación diferencial de primer orden, mediante el 
                                    método de separación de variables, siendo posible encontrar su solución de 
                                    igual forma por el método Bernoulli’s y transformación a una ecuación exacta
                                    """, style={'textAlign': 'justify'}),
                                    html.P(children=[ECUACION_LOGISTICA_RESOLUCION], style={'textAlign': 'center'}),

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

@app.callback(
    [dash.dependencies.Output('formula_generada', 'children'),
    dash.dependencies.Output('grafica_pronostico', 'children')],
    [dash.dependencies.Input('select_column', 'value')])
def muestraGrafica(select_value):

    valor_inicial = DATOS.iloc[0][select_value]
    valor_1 = DATOS.iloc[10][select_value]
    valor_2 = DATOS.iloc[20][select_value]

    con_a = getConstanteA(valor_inicial,valor_1,valor_2)
    con_b = getConstanteB(valor_inicial,valor_1,con_a)
    con_c2 = getConstanteC2(valor_inicial,con_a,con_b)

    Formula = '\[ P(t) = { ' + str(con_a*con_c2) + ' \over ' + str(con_b*con_c2) + '+ e^{ -' + str(con_a) + 't }} \]'
    
    Ecuacion = getcalculo_ecuacion(len(DATOS.index), con_a, con_b, con_c2)

    cLayout = go.Layout(title='Población Mundial',
                        # Same x and first y
                        xaxis_title='Año',
                        yaxis_title='Personas (en millones)',
                        height=450
                        )

    trace1 = go.Scatter(x=DATOS['Año'], y=DATOS['Datos por Defecto'], name='Población Valores Defecto')
    trace2 = go.Scatter(x=DATOS['Año'], y=DATOS['Datos por Defecto sin NRR'], name='Población Valores Defecto (sin NRR)')

    trace4 = go.Scatter(x=DATOS['Año'], y=Ecuacion, name='Población Ecuación Diferencial')

    return Formula,(
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(id='graph', figure={
                                    'data': [trace1,trace2,trace4],
                                    'layout':cLayout
                                })
                            )
                        )
                    ]))


if __name__ == '__main__':
    app.run_server()
