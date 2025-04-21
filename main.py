import yaml
import requests
import time
import sys
import logging
from collections import defaultdict
from urllib.parse import urlparse
import concurrent.futures
import os
from datetime import datetime

# ENHANCEMENT 2: Added daily rotating log file in 'logs' directory
os.makedirs("logs", exist_ok=True)
log_filename = datetime.now().strftime("logs/monitor_%Y-%m-%d.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# Function to load configuration from the YAML file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            if not isinstance(config, list):  #BUG FIX 2 - Validation of YAML format
                raise ValueError("Configuration should be a list of endpoints")
            return config
    except (yaml.YAMLError, FileNotFoundError) as e:
        logger.error(f"Error loading configuration file: {str(e)}") # BUG FIX #5 - Better error logging
        sys.exit(1)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint.get('url')
    if not url:
        logger.error(f"Missing URL for endpoint: {endpoint.get('name', 'unknown')}")  # BUG FIX #4: Handle missing URL
        return "DOWN"
    
    method = endpoint.get('method', 'GET')  # BUG FIX #1 - Default method to GET
    headers = endpoint.get('headers')
    body = endpoint.get('body')
    
    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body if body else None, timeout=0.5)  # BUG FIX #3 - Timeout added
        response_time = time.time() - start_time
        
        # BUG FIX #3 (continued): Check both status code and response time
        if 200 <= response.status_code < 300 and response_time <= 0.5:
            logger.debug(f"{endpoint.get('name', url)} is UP - Status: {response.status_code}, Time: {response_time:.3f}s")
            return "UP"
        else:
            reason = f"Status: {response.status_code}" if response_time <= 0.5 else f"Timeout: {response_time:.3f}s"
            logger.debug(f"{endpoint.get('name', url)} is DOWN - {reason}")
            return "DOWN"
    except requests.RequestException as e:
        logger.debug(f"{endpoint.get('name', url)} is DOWN - Error: {str(e)}")  # BUG FIX #5 - Better error logging
        return "DOWN"


def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.split(':')[0] # BUG FIX #6 - Extract domain and strip port

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    
    logger.info(f"Starting monitoring of {len(config)} endpoints")
    
    while True:
        start_time = time.time()
        check_results = []
        
        # ENHANCEMENT 1 - Added concurrency using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_health, endpoint) for endpoint in config]
            
            for endpoint, future in zip(config, futures):
                domain = extract_domain(endpoint["url"])
                result = future.result()
                
                domain_stats[domain]["total"] += 1
                if result == "UP":
                    domain_stats[domain]["up"] += 1
                
                check_results.append({
                    "domain": domain,
                    "name": endpoint.get("name", endpoint["url"]),
                    "result": result
                })
        
        logger.info("--- Health Check Results ---")
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            logger.info(f"{domain} has {availability}% availability percentage")
        
        # ENHANCEMENT 3: Maintain 15-second intervals between checks
        elapsed_time = time.time() - start_time
        sleep_time = max(0, 15 - elapsed_time)
        logger.debug(f"Check cycle completed in {elapsed_time:.2f}s, sleeping for {sleep_time:.2f}s") # ENHANCEMENT 4: Improved Logging for Success and Errors
        time.sleep(sleep_time)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>") 
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")