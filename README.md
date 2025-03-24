# Kubernetes Cluster Health Monitoring System

## System Overview
A comprehensive monitoring solution that collects Kubernetes cluster metrics, detects anomalies, and prepares for automated remediation (Phase 2). The system currently tracks:

- CPU/Memory utilization
- Network latency
- Pod health status
- Resource allocation

## Key Components

### 1. Core Infrastructure
- **Docker Container**: Pre-configured monitoring environment
- **Prometheus**: Metrics collection and storage
- **Kubernetes Operators**: Stress test deployments
- **Python Data Pipeline**: Metric processing and storage

### 2. Current Capabilities (Phase 1)
- Real-time metric collection from cluster nodes
- Automated CSV dataset generation
- Basic threshold-based alerting
- Stress test integration (CPU/Memory workloads)

### 3. Setup Guide
1. **Prerequisites**: Docker, Kubernetes, and Helm installed
2. **Deployment**:
   - Build monitoring container: `docker build -t k8s-monitor:1.0 .`
   - Launch Prometheus with provided Helm chart
   - Apply Kubernetes manifests from `/kubernetes` directory

### 4. Data Flow
## Exactly How It Works

### Data Collection Process
1. **Every 15 Seconds**:
   - Prometheus gathers metrics from:
     - Node resources (CPU/memory)
     - Pod status
     - Network activity

2. **Data Cleaning**:
   - Python scripts remove empty/unusable data
   - Convert timestamps to readable format
   - Label metrics with node/pod names

3. **Storage**:
   - Creates organized CSV files:
     ```
     datasets/
     ├── cpu_metrics.csv
     ├── memory_metrics.csv  
     └── network_metrics.csv
     ```

### Files  Created
| File | Purpose | Location |
|------|---------|----------|
| `monitor.py` | Main data collector | `scripts/` |
| `prometheus.yml` | Metrics rules | `kubernetes/` | 
| `stress-test.yaml` | Test workloads | `kubernetes/` |

## Phase 2 Roadmap
- Pod Failures → Deletes 50% of running pods.
- Node Failures → Randomly drains Kubernetes nodes.
- Kubelet Kill → Crashes node Kubelet process.
- DNS Failures → Breaks internal networking.
- DDoS Simulation → Sends 1500 fake requests per second.
- Disk Stress → High I/O load & 30% disk corruption.
- Clock Skew → Modifies system time by +15 minutes.
- Random Reboots → Introduces unexpected node crashe

-MACHINE LEARNING:(remaning part of phase 1 )
 - Autoencoder → Detects anomalies in pod resource usage.
 - Graph Neural Networks (GNNs) → Models relationships between pods, nodes, and failures.
 - Explainable AI (SHAP/LIME) → Explains why the failure happened.
 - Visualizations → Time-series failure trends + Cluster-wide dependency graph.

## Usage
```bash
# Start the monitoring pipeline
python3 scripts/start_monitoring.py

# View collected metrics
ls -lh datasets/
