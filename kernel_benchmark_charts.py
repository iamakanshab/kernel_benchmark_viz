import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Sample data - replace this with your actual data loading logic
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

# Calculate total operations
df['total_ops'] = df['M'] * df['N'] * df['K']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("GEMM Kernel Size 2D Visualizer"),
    
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
        dcc.Tab(label='2D Roofline Plot', children=[
            dcc.Graph(id='2d-roofline-plot')
        ]),
        dcc.Tab(label='Performance Heatmap', children=[
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
    [Output('2d-roofline-plot', 'figure'),
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
    
    # 2D Roofline Plot
    roofline_fig = go.Figure()

    # Add scatter plot for kernels
    roofline_fig.add_trace(go.Scatter(
        x=filtered_df['total_ops'],
        y=filtered_df['tflops'],
        mode='markers',
        marker=dict(
            size=filtered_df['K'] / 100,  # Adjust scaling as needed
            color=filtered_df['M'],
            colorscale='Viridis',
            colorbar=dict(title='M Dimension'),
            showscale=True,
        ),
        text=[f"Kernel: {name}<br>M={m}, N={n}, K={k}<br>Total Ops: {ops:,.0f}<br>Performance: {perf:.2f} TFLOP/s"
              for name, m, n, k, ops, perf in zip(filtered_df['name'], filtered_df['M'], 
                                                  filtered_df['N'], filtered_df['K'], 
                                                  filtered_df['total_ops'], filtered_df['tflops'])],
        hoverinfo='text',
        name='Kernels'
    ))

    # Add roof line
    peak_performance = max(filtered_df['tflops']) * 1.1  # 10% above max for visualization
    x_range = np.logspace(np.log10(min(filtered_df['total_ops'])), np.log10(max(filtered_df['total_ops'])), 100)
    roofline_fig.add_trace(go.Scatter(
        x=x_range,
        y=[peak_performance] * len(x_range),
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Peak Performance'
    ))

    roofline_fig.update_layout(
        title='2D Roofline Plot: GEMM Kernel Sizes vs Performance',
        xaxis_title='Total Operations (M * N * K)',
        yaxis_title='Performance (TFLOP/s)',
        xaxis_type='log',
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.5)'),
        height=600
    )
    
    # Heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=[filtered_df['tflops']],
        x=filtered_df['name'],
        y=['Performance'],
        colorscale='Viridis',
        colorbar=dict(title='TFLOP/s')
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
