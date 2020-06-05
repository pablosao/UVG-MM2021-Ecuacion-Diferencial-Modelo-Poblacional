import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

"""
Aplicación de Dash para graficar los datos del crecimiento poblacional y la
rersolución de la ecuación diferencial logistica
:author: Pablo Sao
:date: 04 de junio de 2020
"""

def generaGrafica():

    # Obteniendo los datos
    DATA = pd.read_excel(open('data.xlsx', 'rb'), sheet_name='Datos')

    cLayout = go.Layout(title='Población Mundial',
                        # Same x and first y
                        xaxis_title='Fecha',
                        yaxis_title='Personas (en millones)',
                        height=700
                        )

    trace1 = go.Scatter(x=DATA['Año'], y=DATA['Inicial'], name='Población Valores Defecto')
    trace2 = go.Scatter(x=DATA['Año'], y=DATA['Inicial sin NRR'], name='Población Valores Defecto (sin NRR)')

    return dcc.Graph(id='graph', figure={
                'data': [trace1,trace2],
                'layout': cLayout
            })




# Link Repositorio
LINK_GITHUB = 'https://github.com/psao/UVG-MM2021-Crecimiento-Poblacional'



# Iniciando la aplicacion
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Creando aplicacion de Dash
app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server
#Colocando titulo a la pestania
app.title = 'Población Mundial'


#Layout de la pagina
app.layout = html.Div(children=[

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

        ),label="Gráficas Población Mundial",disabled=False)
    ]),

    html.A('Código en Github', href=LINK_GITHUB),
    html.Br(),


])

if __name__ == '__main__':
    app.run_server()
