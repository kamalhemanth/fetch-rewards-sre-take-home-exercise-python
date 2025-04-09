import yaml
import requests
import time
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    if method is None:
        method = "GET"

    try:
        response = requests.request(method, url, headers=headers, json=body)
        response_time_ms = response.elapsed.total_seconds() * 1000
        if 200 <= response.status_code < 300 and response_time_ms <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            if 'name' and 'url' not in endpoint:
                print("Error: Each endpoint must have a 'url' and 'name'.")
                return
            domain = endpoint["url"].split("//")[-1].split("/")[0]
            domain = domain.split(":")[0]
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)
    if not sys.argv[1].endswith(('.yaml','.yml')):
        print("Error: The config file must be a yaml.")
        sys.exit(1)
    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
