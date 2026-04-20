import time

from config import CHECK_INTERVAL
from monitor import get_system_stats, print_stats
from logger_util import log_stats
from alerts import check_thresholds
from simulator import cpu_stress_test

def main() -> None:
    print("Starting System Monitoring Tool...")
    print("Press Ctrl.C to stop.\n")

    alert_counts = {
        'cpu_percent': 0,
        'memory_percent': 0,
        'disk_percent': 0,
    }

#    simulate = input("Do you want to run a CPU stress test first? (y/n): ").strip().lower()

#    if simulate == 'y':
#        cpu_stress_test(10)

    try:
        while True:
            stats = get_system_stats()
            print_stats(stats)
            log_stats(stats)
            check_thresholds(stats, alert_counts)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == '__main__':
    main()