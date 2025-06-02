# Endpoint Availability Monitoring

A command-line tool written in Python to monitor the availability of HTTP endpoints

## 📋 Overview

This tool checks HTTP endpoints periodically and reports cumulative availability by domain, helping identify reliability trends over time.

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

### Running the endpoint monitor

```bash
python main.py config/endpoints.yaml
```

## 🛠️ Code Changes and Improvements

### Availability Calculation

- **Issue:** The initial code did not calculate the availability cumulatively over time.
- **Solution:** Implemented logic to track the number of "UP" and "DOWN" responses for each domain across multiple check cycles, and calculated the availability as a percentage.

### Response Time Validation

- **Issue:** There was no check for response time, leading to endpoints potentially being marked as "UP" even if they took longer than 500ms to respond.
- **Solution:** Added validation to ensure endpoints are only considered "UP" if its response time is ≤ 500ms.

### Parsing Domains

- **Issue:** Domain names were not parsed correctly
- **Resolution:** Implemented a function that extracts the domain name from the URL while ignoring port numbers.

### 4. Error Handling for Failed Requests

- **Issue:** The initial code did not properly handle failed HTTP requests.
- **Solution:** Added exception handling to catch request failures and classify those endpoints.

---