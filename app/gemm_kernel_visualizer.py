import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Sample data
data = [
    {"name": "Kernel A", "M": 1024, "N": 1024, "K": 1024, "tflops": 100, "batch": 32, "dtype": "f32", "model": "modelX"},
    {"name": "Kernel B", "M": 2048, "N": 2048, "K": 2048, "tflops": 80, "batch": 64, "dtype": "f16", "model": "modelY"},
    {"name": "Kernel C", "M": 4096, "N": 4096, "K": 4096, "tflops": 120, "batch": 32, "dtype": "f32", "model": "modelX"},
    {"name": "Kernel D", "M": 512, "N": 512, "K": 512, "tflops": 90, "batch": 64, "dtype": "f16", "model": "modelY"},
    {"name": "Kernel E", "M": 8192, "N": 8192, "K": 8192, "tflops": 110, "batch": 32, "dtype": "f32", "model": "modelZ"},
    {"name": "Kernel F", "M": 256, "N": 256, "K": 256, "tflops": 70, "batch": 64, "dtype": "f16", "model": "modelX"},
    {"name": "Kernel G", "M": 16384, "N": 16384, "K": 16384, "tflops": 130, "batch": 32, "dtype": "f32", "model": "modelY"},
    {"name": "Kernel H", "M": 1024, "N": 2048, "K": 4096, "tflops": 95, "batch": 64, "dtype": "f16", "model": "modelZ"},
]

df = pd.DataFrame(data)
df['total_ops'] = df['M'] * df['N'] * df['K']
df['arithmetic_intensity'] = 2 * df['K'] / (4 + 4 + 4)  # Assuming single precision

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("GEMM Kernel Visualizer"),
    
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
        dcc.Tab(label='Heatmap', children=[
            dcc.Graph(id='heatmap')
        ]),
        dcc.Tab(label='Split Charts', children=[
            html.Div([
                dcc.Graph(id='size-chart', style={'display': 'inline-block', 'width': '50%'}),
                dcc.Graph(id='performance-chart', style={'display': 'inline-block', 'width': '50%'})
            ])
        ]),
    ])
])

@app.callback(
    [Output('roofline-plot', 'figure'),
     Output('heatmap', 'figure'),
     Output('size-chart', 'figure'),
     Output('performance-chart', 'figure')],
    [Input('batch-dropdown', 'value'),
     Input('dtype-dropdown', 'value'),
     Input('model-dropdown', 'value')]
)
def update_graphs(selected_batch, selected_dtype, selected_model):
    filtered_df = df
    if selected_batch != 'all':
        filtered_df = filtered_df[filtered_df['batch'] == int(selected_batch)]
    if selected_dtype != 'all':
        filtered_df = filtered_df[filtered_df['dtype'] == selected_dtype]
    if selected_model != 'all':
        filtered_df = filtered_df[filtered_df['model'] == selected_model]
    
    # Roofline Plot
    peak_memory_bandwidth = 900  # GB/s, adjust based on your hardware
    peak_compute = 19500  # GFLOP/s, adjust based on your hardware
    x_range = np.logspace(0, 4, 100)
    y_memory = peak_memory_bandwidth * x_range
    y_compute = np.full_like(x_range, peak_compute)
    y_roofline = np.minimum(y_memory, y_compute)

    roofline_fig = go.Figure()
    roofline_fig.add_trace(go.Scatter(
        x=filtered_df['arithmetic_intensity'],
        y=filtered_df['tflops'] * 1000,  # Convert TFLOP/s to GFLOP/s
        mode='markers',
        marker=dict(
            size=10,
            color='blue',  # Single color for all dots
            symbol='circle',
        ),
        text=[f"Kernel: {name}<br>M={m}, N={n}, K={k}<br>Performance: {perf:.2f} TFLOP/s"
              for name, m, n, k, perf in zip(filtered_df['name'], filtered_df['M'], filtered_df['N'], filtered_df['K'], filtered_df['tflops'])],
        hoverinfo='text',
        name='Kernels'
    ))
    roofline_fig.add_trace(go.Scatter(
        x=x_range,
        y=y_roofline,
        mode='lines',
        name='Roofline',
        line=dict(color='red', dash='dash')
    ))
    roofline_fig.update_layout(
        title='Roofline Plot',
        xaxis_title='Arithmetic Intensity (FLOP/byte)',
        yaxis_title='Performance (GFLOP/s)',
        xaxis_type='log',
        yaxis_type='log'
    )
    
    # Heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=[filtered_df['tflops']],
        x=filtered_df['name'],
        y=['Performance'],
        colorscale='Viridis'
    ))
    heatmap_fig.update_layout(
        title='Performance Heatmap',
        xaxis_title='Kernels',
        yaxis_title='Metric'
    )
    
    # Size Chart
    size_fig = go.Figure()
    size_fig.add_trace(go.Bar(x=filtered_df['name'], y=filtered_df['M'], name='M'))
    size_fig.add_trace(go.Bar(x=filtered_df['name'], y=filtered_df['N'], name='N'))
    size_fig.add_trace(go.Bar(x=filtered_df['name'], y=filtered_df['K'], name='K'))
    size_fig.update_layout(
        barmode='group',
        title='Kernel Sizes (M, N, K)',
        xaxis_title='Kernels',
        yaxis_title='Size',
        yaxis_type='log'  # Using log scale for better visualization
    )
    
    # Performance Chart
    perf_fig = go.Figure(data=[
        go.Bar(x=filtered_df['name'], y=filtered_df['tflops'])
    ])
    perf_fig.update_layout(
        title='Performance',
        xaxis_title='Kernels',
        yaxis_title='Performance (TFLOP/s)'
    )
    
    return roofline_fig, heatmap_fig, size_fig, perf_fig

if __name__ == '__main__':
    app.run_server(debug=True, reload=False)
