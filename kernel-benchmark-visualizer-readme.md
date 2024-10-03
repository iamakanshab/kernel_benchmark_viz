# Kernel Benchmark Visualizer

This interactive web application visualizes kernel benchmark data using Python, Dash, and Plotly. It provides multiple views of your benchmark results, including a Roofline Plot, Performance Heatmap, and Split Charts for Arithmetic Intensity and Performance.

## Features

- **Interactive Filtering**: Filter data by batch size, data type, and model.
- **Roofline Plot**: Visualize kernel performance in relation to arithmetic intensity and hardware limits.
- **Performance Heatmap**: Quickly identify high and low performing kernels.
- **Split Charts**: Compare arithmetic intensity and performance across kernels.

## Installation

1. Ensure you have Python 3.7+ installed on your system.
2. Clone this repository or download the `kernel_benchmark_visualizer.py` file.
3. Install the required packages:

```bash
pip install dash pandas plotly numpy
```

## Usage

1. Run the script:

```bash
python kernel_benchmark_visualizer.py
```

2. Open a web browser and go to `http://127.0.0.1:8050/`

## Interactive Plots

### Roofline Plot

![Roofline Plot](https://via.placeholder.com/600x400.png?text=Roofline+Plot)

The Roofline Plot shows:
- Scatter points representing individual kernels
- X-axis: Arithmetic Intensity (FLOP/byte)
- Y-axis: Performance (TFLOP/s)
- Red line: Roofline model combining memory bandwidth and peak compute limits

Interactivity:
- Hover over points to see kernel details
- Use the toolbar to zoom, pan, or reset the view

### Performance Heatmap

![Performance Heatmap](https://via.placeholder.com/600x400.png?text=Performance+Heatmap)

The Heatmap displays:
- Kernels on the X-axis
- Performance intensity represented by color

Interactivity:
- Hover over cells to see exact performance values
- Use the color scale to identify high and low performing kernels

### Split Charts

![Split Charts](https://via.placeholder.com/600x400.png?text=Split+Charts)

The Split Charts show:
1. Arithmetic Intensity Chart:
   - X-axis: Kernels
   - Y-axis: Arithmetic Intensity (FLOP/byte)

2. Performance Chart:
   - X-axis: Kernels
   - Y-axis: Performance (TFLOP/s)

Interactivity:
- Hover over bars to see exact values
- Compare arithmetic intensity and performance side-by-side

## Filtering Data

Use the dropdown menus at the top of the page to filter the data:
- Batch Size
- Data Type (dtype)
- Model

All charts will update automatically based on your selection.

## Customization

To use your own data:
1. Replace the `data` list in the script with your benchmark results.
2. Adjust the `peak_memory_bandwidth` and `peak_compute` variables in the script to match your hardware specifications.

## Troubleshooting

- If the plots don't render, check your internet connection (Plotly requires internet access for some components).
- For Windows users, if you encounter issues with auto-reloading, modify the last line of the script to:

```python
app.run_server(debug=True, use_reloader=False)
```

## Contributing

Contributions to improve the visualizer are welcome! Please submit issues and pull requests on our GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
