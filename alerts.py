from config import (
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    DISK_THRESHOLD,
    CONSECUTIVE_ALERTS_REQUIRED,
)
from logger_util import log_alert

def check_thresholds(stats: dict, alert_counts: dict) -> None:
    """Check whether system stats exceed thresholds."""
    thresholds = {
        'cpu_percent': CPU_THRESHOLD,
        'memory_percent': MEMORY_THRESHOLD,
        'disk_percent': DISK_THRESHOLD,
    }

    for metric, threshold in thresholds.items():
        value = stats[metric]

        if value > threshold:
            alert_counts[metric] += 1
        else:
            alert_counts[metric] = 0
        
        if alert_counts[metric] >= CONSECUTIVE_ALERTS_REQUIRED:
            message = f"ALERT: {metric} is at {value}% (threshold: {threshold}%)"
            print(message)
            log_alert(message)