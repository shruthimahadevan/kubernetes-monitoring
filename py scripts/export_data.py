import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Prometheus server URL
PROMETHEUS_URL = "http://localhost:9090"

# Define queries for each scenario
QUERIES = {
    "cpu_stress": 'rate(container_cpu_usage_seconds_total[5m])',
    "network_latency_receive": 'rate(container_network_receive_bytes_total[5m])',
    "network_latency_transmit": 'rate(container_network_transmit_bytes_total[5m])',
    "memory_stress": 'container_memory_usage_bytes',
    "disk_stress_read": 'rate(container_fs_reads_bytes_total[5m])',
    "disk_stress_write": 'rate(container_fs_writes_bytes_total[5m])',
    "clock_skew": 'node_time_seconds',  # Example metric for clock skew
    "dns_failure": 'kube_dns_error_count_total',  # Example metric for DNS failure
    "random_reboots": 'kube_node_status_condition{condition="Ready"}',
    "random_pod_deletion": 'kube_pod_container_status_restarts_total',
}

# Time range for data collection (e.g., last 5 hours)
DURATION_HOURS = 5
STEP = 60  # 1 minute

# Function to query Prometheus and save data
def collect_prometheus_data():
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=DURATION_HOURS)

    # Convert timestamps to Unix time
    start_unix = int(start_time.timestamp())
    end_unix = int(end_time.timestamp())

    # Collect data for each query
    all_data = []
    for scenario, query in QUERIES.items():
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query_range",
            params={
                "query": query,
                "start": start_unix,
                "end": end_unix,
                "step": STEP,
            }
        )

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error for {scenario}: {response.status_code} - {response.text}")
            continue

        # Parse the response
        data = response.json()

        # Convert to DataFrame
        results = data["data"]["result"]
        for result in results:
            metric = result["metric"]  # Labels (e.g., container name, pod name)
            values = result["values"]  # Time-series data
            for timestamp, value in values:
                all_data.append({
                    "scenario": scenario,
                    "timestamp": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"),
                    "value": float(value),
                    **metric  # Add labels as columns
                })

    # Create DataFrame
    df = pd.DataFrame(all_data)

    # Save to CSV
    df.to_csv("prometheus_stress_data.csv", index=False)
    print(f"Data saved to prometheus_stress_data.csv at {datetime.now()}")

# Run the script for 5 hours
start_time = datetime.now()
end_time = start_time + timedelta(hours=DURATION_HOURS)

while datetime.now() < end_time:
    collect_prometheus_data()
    time.sleep(STEP)  # Wait for 1 minute before the next query