"""
Aplicación de Dash para graficar los datos del crecimiento poblacional y la
rersolución de la ecuación diferencial logistica
:author: Pablo Sao
:date: 04 de junio de 2020
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import math
import base64

def getConstanteA(valor_inicial,observacion_1,observacion_2):
    constante_a = (1/10) * math.log( ( ( (valor_inicial**2) * observacion_2) - observacion_2  ) / ( ( (valor_inicial**2) * observacion_1) - observacion_1  ) )
    return  constante_a

def getConstanteB(valor_inicial,observacion_1,constante_a):
    constante_b = (constante_a * ( (observacion_1 * math.exp(-10*constante_a)) - valor_inicial) )/(observacion_1*valor_inicial*(math.exp(-10*constante_a) - 1))
    return constante_b

def getConstanteC2(valor_inicial,constante_a,constante_b):
    constante_c2 = valor_inicial / (constante_a - (valor_inicial*constante_b))
    return constante_c2


def getcalculo_ecuacion(cantidad_datos,constante_a,constante_b,constante_c2):
    valores = []
    for generar in range(cantidad_datos):
        p = int(round( (constante_a * constante_c2)/( (constante_b * constante_c2) + math.exp(-constante_a * generar)) ))
        valores.append(p)

    return valores




DES_ECUACION_LOGISTICA = \
"""
Zill (2019), indica que aproximadamente en 1840 el matemático y biólogo P. Verhulst 
investigó modelos matemáticos para predecir la población humana en varios países, 
donde las curvas logísticas predicen con bastante exactitud el crecimiento de ciertos 
tipos de bacterias, protozoarios, pulgas de agua y moscas de frutas en ambientes limitados. 
Siendo la ecuación:
"""

METODOLOGIA = \
"""
Para el curso de Ecuaciones Diferenciales de la Universidad del Valle de Guatemala, se 
utilizo el [Simulador de Población Mundial de Roehr (s.f.)](http://fightoverpopulation.org/), 
para la obtención de los datos experimentales. Recolectando el valor de población (en millones) 
desde el año 1900 hasta el año 2019. Y así resolver la Ecuación Lógistica.
"""

REFERENCIAS = \
""" 
Roehr, C. (s.f.). *World Population Simulator*. Extraído de: [http://fightoverpopulation.org/](http://fightoverpopulation.org/)

Zill, D. (2018). *Ecuaciones Diferenciales con aplicaciones de modelado*. Toluca, Ciudad de México: CENGAGE. 23 – 24 pp.
"""

# Ecuaciones de información
ECUACION_LOGISTICA = "\[ { dP \over dt} = P(a - bP) \]"
ECUACION_LOGISTICA_RESOLUCION = "\[ P(t) = { aC_2 \over bC_2 + e^{-at}} \]"

# Link Repositorio
LINK_GITHUB = 'https://github.com/psao/UVG-MM2021-Ecuacion-Diferencial-Modelo-Poblacional'

# Logo universidad del Valle de Guatemala
file_uvg_logo = 'uvg-logo.jpg' # replace with your own image
UVG_LOGO = base64.b64encode(open(file_uvg_logo, 'rb').read())

ECUACION_CUSTOMIZADA = ''

# leyendo datos de Excel
DATOS = pd.read_excel('data.xlsx', sheet_name='Datos')

# Find the columns where each value is null
empty_cols = [col for col in DATOS.columns if DATOS[col].isnull().all()]
# Drop these columns from the dataframe
DATOS.drop(empty_cols,
        axis=1,
        inplace=True)


# Obteniendo nombre de las columnas
OPCIONES = list(DATOS.columns)
OPCIONES.remove('Año')

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
        [
            dbc.Col(
                html.Img(src='data:image/png;base64,{}'.format(UVG_LOGO.decode()),style={'width': '125px'}),
                width={"size": 2, "order": 1, "offset": 1},
            ),
            dbc.Col(
                (
                    html.Br(),
                    html.H1(children='Población Mundial'),
                    html.H4(children='Pablo Sao & Shirley Marroquín'),
                ),
                width={"size": 3, "order": 2},
            ),
            dbc.Col(
                (
                    html.Br(),
                    html.Br(),
                    html.A('Código en Github', href=LINK_GITHUB),
                ),
                width={"size": 3, "order": 3},
            ),
        ]
    ),

    html.Br(),

    dbc.Row(
        [
            dbc.Col((
                dbc.Tabs([

                    # Informacion
                    dbc.Tab((

                            dbc.CardBody(
                                dbc.CardBody([
                                    html.P(dcc.Markdown(METODOLOGIA),style={'textAlign': 'justify'}),


                                    html.H3(children='Ecuación Logística'),

                                    html.P(DES_ECUACION_LOGISTICA, style={'textAlign': 'justify'}),

                                    html.P(children=[ECUACION_LOGISTICA], style={'textAlign': 'center'}),

                                    html.P(
                                    """
                                    Primero se determinó la ecuación diferencial de primer orden, mediante el 
                                    método de separación de variables, siendo posible encontrar su solución de 
                                    igual forma por el método Bernoulli’s y transformación a una ecuación exacta.
                                    """, style={'textAlign': 'justify'}),

                                    html.P(children=[ECUACION_LOGISTICA_RESOLUCION], style={'textAlign': 'center'}),

                                    html.Div(id='formula_generada_mostrar'),

                                    html.Br(),
                                    html.H3(children='Referencias en este sitio'),

                                    dcc.Markdown(REFERENCIAS),

                                ]),
                                className='mt-3'
                            )

                        ),label="Información",disabled=False),

                    # Grafica
                    dbc.Tab((
                        dbc.CardBody(
                            dbc.CardBody([

                                dbc.Row([
                                    dbc.Col(
                                        html.Div(children='''Datos para Construir Ecuación:'''),
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
                                dbc.Row(
                                    dbc.Col(
                                        html.Div(id='grafica_pronostico'),
                                        width={"size": 12, "order": 1}
                                    )
                                ),


                            ]),
                            className='mt-3'
                        )
                    ),label="Gráficas Población Mundial",disabled=False),






                ]),
            ),
            width={"size": 10, "offset": 1}),
        ]
    ),
])

@app.callback(
    [dash.dependencies.Output('formula_generada', 'children'),
    dash.dependencies.Output('formula_generada_mostrar', 'children'),
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

    datos_info = "Los datos utilizados para encontrar las constantes fueron: t = 0, P(0) = {0}." \
                 " t = 10, P(10) = {1}. t = 20, P(20) = {2}. Determinando la ecuación".format(
        valor_inicial,valor_1,valor_2
    )

    Ecuacion = getcalculo_ecuacion(len(DATOS.index), con_a, con_b, con_c2)

    cLayout = go.Layout(title='Población Mundial',
                        # Same x and first y
                        xaxis_title='Año',
                        yaxis_title='Personas (en millones)',
                        width = 1020, height=450
                        )

    TRACE = [go.Scatter(x=DATOS['Año'], y=Ecuacion, name='Calculado con Ecuación Diferencial')]

    for name in OPCIONES:
        TRACE.append(go.Scatter(x=DATOS['Año'], y=DATOS[name], name=name))

    #trace1 = go.Scatter(x=DATOS['Año'], y=DATOS['Datos por Defecto'], name='Población Valores Defecto')
    #trace2 = go.Scatter(x=DATOS['Año'], y=DATOS['Datos por Defecto sin NRR'], name='Población Valores Defecto (sin NRR)')


    return Formula,\
                (
                    html.Div((
                        html.P(datos_info, style={'textAlign': 'justify'}),
                        html.Br(),
                        html.P(children=[Formula], style={'textAlign': 'center'}),
                    ))
                ),\
                (
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(id='graph', figure={
                                    'data': TRACE,
                                    'layout':cLayout
                                })
                            )
                        )
                    ])
                )


if __name__ == '__main__':
    app.run_server()
