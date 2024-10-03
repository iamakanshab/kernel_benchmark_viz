
# Kernel Benchmark Visualizer

Kernel Benchmark Visualizer is a web-based dashboard for visualizing and analyzing the performance of General Matrix Multiplication (GEMM) kernels. It provides interactive visualizations including a Roofline plot, performance heatmap, and size comparisons of different GEMM kernels.

## Features

- Interactive Roofline Plot
- Performance Heatmap
- Kernel Size Comparison Charts
- Filtering by batch size, data type, and model
- Kubernetes-ready deployment

## Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster (for deployment)
- kubectl

## Directory Structure

```
gemm-kernel-visualizer/
│
├── app/
│   ├── gemm_kernel_visualizer.py
│   └── requirements.txt
│
├── kubernetes/
│   └── deployment.yaml
│
├── Dockerfile
│
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gemm-kernel-visualizer.git
   cd gemm-kernel-visualizer
   ```

2. Install the required Python packages:
   ```
   pip install -r app/requirements.txt
   ```

## Local Usage

To run the application locally:

1. Navigate to the `app` directory:
   ```
   cd app
   ```

2. Run the Python script:
   ```
   python gemm_kernel_visualizer.py
   ```

3. Open a web browser and go to `http://127.0.0.1:8050/` to view the dashboard.

## Docker Build

To build the Docker image:

1. Ensure you're in the root directory of the project.

2. Build the image:
   ```
   docker build -t gemm-kernel-visualizer:latest .
   ```

3. Run the container locally (optional):
   ```
   docker run -p 8050:8050 gemm-kernel-visualizer:latest
   ```

## Kubernetes Deployment

To deploy the application to a Kubernetes cluster:

1. Push the Docker image to a container registry:
   ```
   docker tag gemm-kernel-visualizer:latest your-registry/gemm-kernel-visualizer:latest
   docker push your-registry/gemm-kernel-visualizer:latest
   ```

2. Update the `kubernetes/deployment.yaml` file with your image name.

3. Apply the Kubernetes deployment:
   ```
   kubectl apply -f kubernetes/deployment.yaml
   ```

4. Check the deployment status:
   ```
   kubectl get deployments
   kubectl get pods
   kubectl get services
   ```

5. Access the application:
   - If using Minikube: `minikube service gemm-kernel-visualizer-service`
   - If using a cloud provider, check the external IP of the LoadBalancer service

## Customization

To customize the visualizations or add new features:

1. Modify the `app/gemm_kernel_visualizer.py` file.
2. Update the `app/requirements.txt` if you add new dependencies.
3. Rebuild the Docker image and redeploy if necessary.

# RUNNING LOCALLY 

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

The Roofline Plot shows:
- Scatter points representing individual kernels
- X-axis: Arithmetic Intensity (FLOP/byte)
- Y-axis: Performance (TFLOP/s)
- Red line: Roofline model combining memory bandwidth and peak compute limits

Interactivity:
- Hover over points to see kernel details
- Use the toolbar to zoom, pan, or reset the view

### Performance Heatmap

The Heatmap displays:
- Kernels on the X-axis
- Performance intensity represented by color

Interactivity:
- Hover over cells to see exact performance values
- Use the color scale to identify high and low performing kernels

### Split Charts

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
