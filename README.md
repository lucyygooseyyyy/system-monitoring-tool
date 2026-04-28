# System Monitoring Tool

A Python tool for monitoring system performance and basic network connectivity.

## Features

* CPU, memory, and disk usage tracking (`psutil`)
* Threshold-based alerts
* Logging of performance data
* Network diagnostics:

  * Gateway reachability
  * Internet reachability
  * Latency checks
* Combined system + network monitoring

## How to Run

```bash
pip install psutil
python main.py
```

## Options

```text
1. System diagnostics
2. Network diagnostics
3. Combined monitoring
```

## Why I Built This

Built to learn system monitoring concepts and extended to debug real issues with a home gateway (intermittent drops, latency spikes, connectivity problems).

## Tech

* Python
* psutil
* subprocess (ping)
* logging
