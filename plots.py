import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import plotly.express as px
import pandas as pd

# Supongamos que tienes una lista de IDs de instancia
instance_ids = ['instance1', 'instance2', 'instance3']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        id='parametros',
        children=[
            html.H1('Parametros'),
            html.Div(id='output-container'),
            html.Div(
                className='grid-container',
                children=[
                    html.Div(
                        children=[
                            html.Label('Min Instances'),
                            dcc.Input(id='min-instances', type='number', placeholder='Min Instances', value=2)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Max Instances'),
                            dcc.Input(id='max-instances', type='number', placeholder='Max Instances', value=5)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('CPU Up Threshold'),
                            dcc.Input(id='cpu-up-threshold', type='number', placeholder='CPU Up Threshold', value=70)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('CPU Down Threshold'),
                            dcc.Input(id='cpu-down-threshold', type='number', placeholder='CPU Down Threshold', value=20)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Scale Up Factor'),
                            dcc.Input(id='scale-up-factor', type='number', placeholder='Scale Up Factor', value=2)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Scale Down Factor'),
                            dcc.Input(id='scale-down-factor', type='number', placeholder='Scale Down Factor', value=0.5),
                        ]
                    ),
                ]
            ),
            html.Button('Guardar', id='guardar-button')
        ]
    ),
    html.H1('Instancias'),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),  # Actualiza cada 5 segundos
    html.Div(id='graphs-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('guardar-button', 'n_clicks')],
    [State('min-instances', 'value'),
     State('max-instances', 'value'),
     State('cpu-up-threshold', 'value'),
     State('cpu-down-threshold', 'value'),
     State('scale-up-factor', 'value'),
     State('scale-down-factor', 'value')]
)
def guardar_configuracion(n_clicks, min_instances, max_instances, cpu_up_threshold, cpu_down_threshold, scale_up_factor, scale_down_factor):
    if n_clicks:
        # Aquí puedes realizar las acciones que deseas con los valores obtenidos
        # por ejemplo, guardarlos en la base de datos o realizar algún procesamiento adicional
        print(f'Min Instances: {min_instances}') #Datos no vacios.
        print(f'Max Instances: {max_instances}')
        print(f'CPU Up Threshold: {cpu_up_threshold}')
        print(f'CPU Down Threshold: {cpu_down_threshold}')
        print(f'Scale Up Factor: {scale_up_factor}')
        print(f'Scale Down Factor: {scale_down_factor}')
        # Puedes devolver un mensaje o cualquier otro contenido que desees mostrar
        return html.Label('Datos guardados correctamente.')

    # Si no se ha hecho clic en el botón, no se muestra ningún mensaje
    return None

@app.callback(Output('graphs-container', 'children'), Input('interval-component', 'n_intervals'))
def update_graphs(n):
    graphs = []
    for instance_id in instance_ids:
        # Aquí, en lugar de utilizar datos ficticios como en el ejemplo,
        # debes utilizar tu lógica para obtener los datos de uso de CPU
        # desde tu base de datos MongoDB y actualizar el DataFrame `df`.

        # Ejemplo ficticio de actualización del DataFrame para cada instancia
        data = {#Agregar los datos de la ultima instancia porque fue la más reciente a cuando se hace el promedio
            'Time': ['2023-05-16 10:00:00', '2023-05-16 10:01:00', '2023-05-16 10:02:00'],
            'cpu_usage': [80, 90, 70],
            'instance_id': [instance_id] * 3
        }

        df = pd.DataFrame(data)

        # Crea la gráfica de líneas con Plotly Express para cada instancia
        fig = px.line(df, x='Time', y='cpu_usage')
        fig.update_traces(
            line=dict(color='blue', width=2),
            marker=dict(color='blue', size=6),
        )

        fig.update_layout(
            title='Consumo de CPU',
            xaxis=dict(
                title='Tiempo',
                showgrid=False,
                zeroline=False,
                showline=True,
                linecolor='black',
                linewidth=1,
                mirror=True
            ),
            yaxis=dict(
                title='Uso de CPU',
                showgrid=True,
                gridcolor='lightgray',
                zeroline=False,
                showline=True,
                linecolor='black',
                linewidth=1,
                mirror=True
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family='Arial',
                size=12,
                color='black'
            ),
            margin=dict(l=40, r=20, t=40, b=20),
        )

        # Agrega la gráfica al contenedor de gráficas
        graphs.append(
            html.Div([
                html.H3(f'Instance ID: {instance_id}'),
                dcc.Graph(figure=fig)
            ])
        )

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
