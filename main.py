import yaml
import requests
import time
import logging
import traceback
from urllib.parse import urlparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG_TIMEOUT = int(os.getenv("CONFIG_TIMEOUT", 10))
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", 15))
LOG_FILE = os.getenv("LOG_FILE", "monitor.log")


# Set up rotating log handler
def setup_logging():
    logger = logging.getLogger("HealthMonitor")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logging()


# Load config from YAML
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load config file: {e}, Please check yaml file should exist in the same root location where the python script is present")
        raise


# Perform individual health check
def check_health(endpoint):
    url = endpoint.get('url')
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    if not url:
        logger.warning("Skipping endpoint with missing URL.")
        return None, "INVALID"

    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=CONFIG_TIMEOUT)
        print(f"Request to {url} took {response.elapsed.total_seconds()} seconds", response.status_code)
        status = "UP" if 200 <= response.status_code < 300 else "DOWN"
        logger.info(f"[{url}] Status: {status} (HTTP {response.status_code})")
        return url, status
    except requests.Timeout:
        logger.warning(f"[{url}] Request timed out.")
        return url, "DOWN"
    except requests.RequestException as e:
        logger.error(f"[{url}] Request failed: {e}")
        return url, "DOWN"
    except Exception:
        logger.error(f"[{url}] Unexpected error:\n{traceback.format_exc()}")
        return url, "DOWN"


# Extract domain from URL
def extract_domain(url):
    try:
        return urlparse(url).netloc
    except Exception:
        return "unknown"


# Main monitoring loop
def monitor_endpoints(file_path):
    config = load_config(file_path)

    # Initialize availability stats
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_endpoint = {
                executor.submit(check_health, endpoint): endpoint for endpoint in config
            }

            for future in as_completed(future_to_endpoint):
                url, status = future.result()
                if url is None:
                    continue
                domain = extract_domain(url)
                domain_stats[domain]["total"] += 1
                if status == "UP":
                    domain_stats[domain]["up"] += 1

        # Log availability per domain
        # ...existing code...
        # Log availability per domain
        for domain, stats in domain_stats.items():
            total = stats["total"]
            up = stats["up"]
            availability = round(100 * up / total) if total > 0 else 0

            if availability == 100:
                status = "UP"
            elif availability == 0:
                status = "DOWN"
            else:
                status = "PARTIAL"

            logger.info(f"  - {domain:<35} ➤  {availability:>3}% {status}")

        logger.info("\n✅ Monitoring cycle complete.\n" + "-" * 60 + "\n")

        elapsed = time.time() - start_time
        sleep_time = max(0, MONITOR_INTERVAL - elapsed)
        time.sleep(sleep_time)


# Entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")
        print("\nMonitoring stopped.")