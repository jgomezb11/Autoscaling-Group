import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from pymongo import MongoClient
import os

client = MongoClient(
    "mongodb://" + os.getenv("IPMONGO") + ":" + os.getenv("PORTMONGO")
)
database = client["ASG"]
collection = database["config"]

last_value_average = 0
global min_i, max_i, cpu_up, cpu_down, scale_up, scale_down
status = collection.find_one()
min_i = status["min_instances"]
max_i = status["max_instances"]
cpu_up = status["cpu_up_threshold"]
cpu_down = status["cpu_down_threshold"]
scale_up = status["scale_up_factor"]
scale_down = status["scale_down_factor"]

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
                            dcc.Input(id='min-instances', type='number', placeholder='Min Instances', value=min_i)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Max Instances'),
                            dcc.Input(id='max-instances', type='number', placeholder='Max Instances', value=max_i)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('CPU Up Threshold'),
                            dcc.Input(id='cpu-up-threshold', type='number', placeholder='CPU Up Threshold', value=cpu_up)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('CPU Down Threshold'),
                            dcc.Input(id='cpu-down-threshold', type='number', placeholder='CPU Down Threshold', value=cpu_down)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Scale Up Factor'),
                            dcc.Input(id='scale-up-factor', type='number', placeholder='Scale Up Factor', value=scale_up)
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Label('Scale Down Factor'),
                            dcc.Input(id='scale-down-factor', type='number', placeholder='Scale Down Factor', value=scale_down),
                        ]
                    ),
                ]
            ),
            html.Button('Guardar', id='guardar-button')
        ]
    ),
    html.H1('Instancias'),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
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
        changes = {}
        if min_instances != None:
            changes["min_instances"] = min_instances
        if max_instances != None:
            changes["max_instances"] = max_instances
        if cpu_up_threshold != None:
            changes["cpu_up_threshold"] = cpu_up_threshold
        if cpu_down_threshold != None:
            changes["cpu_down_threshold"] = cpu_down_threshold
        if scale_up_factor != None:
            changes["scale_up_factor"] = scale_up_factor
        if scale_down_factor != None:
            changes["scale_down_factor"] = scale_down_factor
        if len(changes) != 0:
            config = collection.find_one()
            response = collection.update_one(
                {'_id': config['_id']},
                {'$set': changes}
            )
            while not response.acknowledged:
                response = collection.update_one(
                    {'_id': config['_id']},
                    {'$set': changes}
                )
        return html.Label(id='label-output', children='Datos guardados correctamente.')

    return None

@app.callback(Output('graphs-container', 'children'), Input('interval-component', 'n_intervals'))
def update_graphs(n):
    global last_value_average
    graphs = []
    status = collection.find_one()["status"]
    n = 0
    average = 0
    for instance_status in status:
        n = len(instance_status["memory_usage"])
        average += instance_status["memory_usage"][-1]
        data = {
            'Time': instance_status["time_stap"],
            'cpu_usage': instance_status["memory_usage"],
            'instance_id': [instance_status["id_instance"]] * n
        }
        df = pd.DataFrame(data)
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
        graphs.append(
            html.Div([
                html.H3(f'Instance ID: {instance_status["id_instance"]}'),
                dcc.Graph(figure=fig)
            ])
        )
    n = len(status)
    fig_gauge  = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        delta ={
            'reference': last_value_average,
            'increasing': {'color': "Red"},
            'decreasing': {'color': 'Green'}
        },
        value=average/n,
        title={'text': "Promedio de uso de CPU"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 30], 'color': "Green"},
                {'range': [30, 50], 'color': "Yellow"},
                {'range': [50, 70], 'color': "Orange"},
                {'range': [70, 100], 'color': "Red"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 5},
                'thickness': 1,
                'value': average/n
            }
        }
    ))
    last_value_average = average/n
    graphs.insert(
        0,
        html.Div([
            html.H3('Uso promedio'),
            dcc.Graph(figure=fig_gauge)
        ])
    )
    return graphs

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
