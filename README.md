# Kubernetes Failure Prediction & Auto-Remediation System

## 📦 Complete Setup Guide

### 1. Prerequisites Installation
```bash
# Install Docker, kubectl, and Helm
curl -fsSL https://get.docker.com | sh
sudo apt-get install -y kubectl helm

# Clone repository
git clone https://github.com/yourusername/kubernetes-monitoring.git
cd kubernetes-monitoring

# Create folder structure
mkdir -p {docker,kubernetes,scripts,datasets}

#docker setup
# docker/Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "monitor.py"]
docker build -t k8s-monitor:1.0 -f docker/Dockerfile .
docker run -d k8s-monitor:1.0

# run the cluster 
kubectl apply -f kubernetes/deployment.yaml

#set up prometheus connection
# kubernetes/prometheus-values.yaml
server:
  persistentVolume:
    enabled: true
alertmanager:
  enabled: true

#collect the data from pormetheus and store it in csv fromat 
# scripts/collect.py
import requests
import pandas as pd

PROM_URL = "http://prometheus:9090"
METRICS = [
    'container_cpu_usage_seconds_total',
    'container_memory_usage_bytes'
]

def fetch_metrics():
    for metric in METRICS:
        response = requests.get(f"{PROM_URL}/api/v1/query?query={metric}")
        pd.DataFrame(response.json()).to_csv(f"datasets/{metric}.csv")