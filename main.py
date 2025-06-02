import yaml
import requests
import time
from collections import defaultdict
import logging
from urllib.parse import urlparse

# Function to load configuration from the YAML file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        e.error("Failed to load file please check to ensure that file is passed: {e}")
        raise

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        elapsed_time = (time.time() - start) * 1000

        print(f"{url} responded in {int(elapsed_time)}ms with status {response.status_code}")

        if 199 < response.status_code < 300 and elapsed_time <= 500:
            return "UP"
        else:
            return "DOWN"
    #improper error handling mistake one
    except requests.RequestException as e:
        print(f"{url} failed to connect: {e}")
        return "DOWN"

#New function that ignores port numbers while parsing domain
def parse_domain(url):
    new_url = urlparse(url)
    return new_url.hostname

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = parse_domain(endpoint['url'])
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round((stats["up"] / stats["total"]) * 100)
            print(f"{domain} has {availability}% availability percentage")

        print("--" * 20)
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")