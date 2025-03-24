import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Prometheus server URL
PROMETHEUS_URL = "http://localhost:9090"

# Queries for each scenario
QUERIES = {
    "clock_skew": '(node_time_seconds - time())',
    "dns_failure_errors": 'kube_dns_error_count_total',
    "dns_failure_queries": 'kube_dns_query_count_total',
    "random_reboots": 'kube_node_status_condition{condition="Ready"}',
    "random_pod_deletion": 'kube_pod_container_status_restarts_total',
}

# Time range for data collection (5 hours)
DURATION_HOURS = 5
STEP = 60  # 1 minute

# Function to collect data
def collect_metrics():
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
        results = data["data"]["result"]

        # Convert to DataFrame
        for result in results:
            metric = result["metric"]  # Labels (e.g., node, pod, namespace)
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
    df.to_csv("stress_metrics_data.csv", index=False)
    print(f"Data saved to stress_metrics_data.csv at {datetime.now()}")

# Run the script for 5 hours
start_time = datetime.now()
end_time = start_time + timedelta(hours=DURATION_HOURS)

while datetime.now() < end_time:
    collect_metrics()
    time.sleep(STEP)  # Wait for 1 minute before the next query