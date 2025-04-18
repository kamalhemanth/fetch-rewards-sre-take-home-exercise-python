import yaml
import requests
import time
from collections import defaultdict
from urllib.parse import urlparse
import time as t

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start = t.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        elapsed_ms = (t.time() - start) * 1000

        print(f"{url} responded in {int(elapsed_ms)}ms with status {response.status_code}")

        if 200 <= response.status_code < 300 and elapsed_ms <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        return "DOWN"

# Function to extract domain name from URL (ignoring ports)
def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    return domain

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = get_domain(endpoint["url"])
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

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
