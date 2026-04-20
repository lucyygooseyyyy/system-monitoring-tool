from datetime import datetime
import psutil
from config import DISK_PATH

def get_system_stats() -> dict:
    """Collect system usage statistics and return them in a dictionary."""
    stats = {
        'timestamp': datetime.now().isoformat(timespec='seconds'),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage(DISK_PATH).percent,
    }
    return stats

def print_stats(stats: dict) -> None:
    """Display the current system stats in the terminal."""
    print(
        f"[{stats['timestamp']}] "
        f"CPU: {stats['cpu_percent']}% | "
        f"Memory: {stats['memory_percent']}% | "
        f"Disk: {stats['disk_percent']}%"
    )