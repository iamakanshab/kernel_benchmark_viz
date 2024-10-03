import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Sample data - replace this with your actual data loading logic
data = [
    {"name": "Kernel A", "arithmeticIntensity": 2.5, "tflops": 100, "batch": 32, "dtype": "f32", "model": "modelX"},
    {"name": "Kernel B", "arithmeticIntensity": 1.8, "tflops": 80, "batch": 64, "dtype": "f16", "model": "modelY"},
    {"name": "Kernel C", "arithmeticIntensity": 3.2, "tflops": 120, "batch": 32, "dtype": "f32", "model": "modelX"},
    {"name": "Kernel D", "arithmeticIntensity": 2.1, "tflops": 90, "batch": 64, "dtype": "f16", "model": "modelY"},
    {"name": "Kernel E", "arithmeticIntensity": 2.8, "tflops": 110, "batch": 32, "dtype": "f32", "model": "modelZ"},
    {"name": "Kernel F", "arithmeticIntensity": 1.5, "tflops": 70, "batch": 64, "dtype": "f16", "model": "modelX"},
    {"name": "Kernel G", "arithmeticIntensity": 3.5, "tflops": 130, "batch": 32, "dtype": "f32", "model": "modelY"},
    {"name": "Kernel H", "arithmeticIntensity": 2.3, "tflops": 95, "batch": 64, "dtype": "f16", "model": "modelZ"},
]

df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Kernel Benchmark Dashboard"),
    
    html.Div([
        dcc.Dropdown(
            id='batch-dropdown',
            options=[{'label': 'All Batches', 'value': 'all'}] + 
                    [{'label': str(b), 'value': b} for b in df['batch'].unique()],
            value='all'
        ),
        dcc.Dropdown(
            id='dtype-dropdown',
            options=[{'label': 'All Dtypes', 'value': 'all'}] + 
                    [{'label': d, 'value': d} for d in df['dtype'].unique()],
            value='all'
        ),
        dcc.Dropdown(
            id='model-dropdown',
            options=[{'label': 'All Models', 'value': 'all'}] + 
                    [{'label': m, 'value': m} for m in df['model'].unique()],
            value='all'
        ),
    ], style={'width': '50%', 'display': 'flex', 'justifyContent': 'space-between'}),
    
    dcc.Tabs([
        dcc.Tab(label='Roofline Plot', children=[
            dcc.Graph(id='roofline-plot')
        ]),
        dcc.Tab(label='Split Charts', children=[
            html.Div([
                dcc.Graph(id='arithmetic-intensity-chart', style={'display': 'inline-block', 'width': '50%'}),
                dcc.Graph(id='performance-chart', style={'display': 'inline-block', 'width': '50%'})
            ])
        ]),
        dcc.Tab(label='Heatmap', children=[
            dcc.Graph(id='heatmap')
        ]),
    ])
])

@app.callback(
    [Output('roofline-plot', 'figure'),
     Output('arithmetic-intensity-chart', 'figure'),
     Output('performance-chart', 'figure'),
     Output('heatmap', 'figure')],
    [Input('batch-dropdown', 'value'),
     Input('dtype-dropdown', 'value'),
     Input('model-dropdown', 'value')]
)
def update_graphs(selected_batch, selected_dtype, selected_model):
    filtered_df = df
    if selected_batch != 'all':
        filtered_df = filtered_df[filtered_df['batch'] == selected_batch]
    if selected_dtype != 'all':
        filtered_df = filtered_df[filtered_df['dtype'] == selected_dtype]
    if selected_model != 'all':
        filtered_df = filtered_df[filtered_df['model'] == selected_model]
    
    # Roofline Plot
    roofline_fig = go.Figure()
    roofline_fig.add_trace(go.Scatter(
        x=filtered_df['arithmeticIntensity'],
        y=filtered_df['tflops'],
        mode='markers',
        text=filtered_df['name'],
        hoverinfo='text+x+y',
        name='Kernels'
    ))
    roofline_fig.update_layout(
        title='Roofline Plot',
        xaxis_title='Arithmetic Intensity',
        yaxis_title='Performance (TFLOP/s)',
        xaxis_type='log',
        yaxis_type='log'
    )
    
    # Arithmetic Intensity Chart
    ai_fig = go.Figure()
    ai_fig.add_trace(go.Bar(
        x=filtered_df['name'],
        y=filtered_df['arithmeticIntensity'],
        name='Arithmetic Intensity'
    ))
    ai_fig.update_layout(
        title='Arithmetic Intensity',
        xaxis_title='Kernel',
        yaxis_title='Arithmetic Intensity'
    )
    
    # Performance Chart
    perf_fig = go.Figure()
    perf_fig.add_trace(go.Bar(
        x=filtered_df['name'],
        y=filtered_df['tflops'],
        name='Performance'
    ))
    perf_fig.update_layout(
        title='Performance',
        xaxis_title='Kernel',
        yaxis_title='Performance (TFLOP/s)'
    )
    
    # Heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=[filtered_df['arithmeticIntensity'], filtered_df['tflops']],
        x=filtered_df['name'],
        y=['Arithmetic Intensity', 'Performance'],
        hoverongaps=False,
        colorscale='Viridis'
    ))
    heatmap_fig.update_layout(
        title='Heatmap of Arithmetic Intensity and Performance',
        xaxis_title='Kernel',
        yaxis_title='Metric'
    )
    
    return roofline_fig, ai_fig, perf_fig, heatmap_fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
