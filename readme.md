# Site Reliability Engineering - Endpoint Availability Monitor

This is a command-line tool written in Python to monitor the availability of HTTP endpoints, as part of the Fetch Rewards Site Reliability Engineering take-home exercise.

## 📋 Overview

As a Site Reliability Engineer, it's important to monitor service uptime and build processes that help others identify and respond to incidents. This tool checks HTTP endpoints periodically and reports cumulative availability by domain, helping identify reliability trends over time.

---

## ✅ Features

- Accepts configuration via a YAML file.
- Periodic health checks every 15 seconds.
- Availability calculated **cumulatively** per domain.
- Endpoints are considered **available** only if:
  - HTTP status code is between `200` and `299`.
  - Response time is `≤ 500ms`.
- Port numbers in URLs are ignored when grouping by domain.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `pip` for managing dependencies
- (Optional but recommended) a virtual environment

### Install Dependencies

```bash
pip install -r requirements.txt
```

or manually

```bash
pip install requests pyyaml
```

### ✅ Check for endpoints.yaml

If config/endpoints.yaml file doesn't exist then create a YAML file like config/endpoints.yaml:

```bash
- name: Google
  url: https://www.google.com
- name: HTTPBin
  url: https://httpbin.org/status/200
  method: GET
```

### Run the Montior

```bash
python main.py config/endpoints.yaml
```

### Your output should look like

![Monitor Output](sre-take-home-exercise-python/output/Output.png)
