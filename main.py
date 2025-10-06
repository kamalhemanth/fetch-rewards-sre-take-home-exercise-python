import yaml
import requests
import time
import sys
import os
from collections import defaultdict
from urllib.parse import urlparse

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', "GET")
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')
    
    start_time = time.time()

    try:
        response = requests.request(method, url, headers=headers, data = body, timeout=0.5)
        elapsed_ms = (time.time() - start_time) * 1000
        if 200 <= response.status_code < 300 and elapsed_ms <= 500:
            return "True"
        else:
            return "False"
    except requests.RequestException:
        return "False"

# Extract domain only
def extract_domain(url):
    parsed = urlparse(url)
    return parsed.hostname

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    
    print("Starting endpoint monitoring (press Ctrl+C to stop)...")

    while True:
        
        cycle_start = time.time()
        
        for endpoint in config:
            domain = extract_domain(endpoint["url"])
            success = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if success:
                domain_stats[domain]["up"] += 1

        print("\n=== Availability Report ===")
        for domain, stats in domain_stats.items():
            if stats["total"] == 0:
                availability = 0
            else:
                availability = int((stats["up"] / stats["total"]) * 100)  # drop decimals
            print(f"{domain}: {availability}% availability")
        print("===========================\n")

        # Ensure each check cycle starts exactly every 15s
        elapsed = time.time() - cycle_start
        sleep_time = max(0, 15 - elapsed)
        time.sleep(sleep_time)

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")