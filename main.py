import time

from config import CHECK_INTERVAL, PING_TARGET
from monitor import get_system_stats, print_stats
from logger_util import log_stats
from alerts import check_thresholds
#from simulator import cpu_stress_test
from network_alerts import check_network_alerts
from network_monitor import get_network_stats, get_default_gateway

def run_system_monitor() -> None:
    """Run CPU, memory and disk monitoring."""
    print('\nRunnning system diagnostics...')
    print('Press Ctrl+C to stop.\n')

    alert_counts = {
        'cpu_percent': 0,
        'memory_percent': 0,
        'disk_percent': 0
    }

    try:
        while True:
            stats = get_system_stats()
            print_stats(stats)
            log_stats(stats)
            check_thresholds(stats, alert_counts)

            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped system diagnostics.")

def run_network_monitor() -> None:
    """Run gateway and internet connectivity monitoring."""
    print("\nRunning network diagnostics...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            gateway_ip = get_default_gateway()
#            print(f"DEBUG gateway_ip = {gateway_ip}")

            if gateway_ip is None:
                print("Could not detect default gateway.")
                return

            print(f"Detected default gateway: {gateway_ip}")

            network_stats = get_network_stats(gateway_ip, PING_TARGET)

            print(
                f"[NETWORK] "
                f"Gateway Reachable: {network_stats['gateway_reachable']} | "
                f"Gateway Latency: {network_stats['gateway_latency_ms']} ms | "
                f"Internet Reachable: {network_stats['internet_reachable']} | "
                f"Internet Latency: {network_stats['internet_latency_ms']} ms"
            )

            if network_stats["gateway_error"]:
                print(f"Gateway Error: {network_stats['gateway_error']}")

            if network_stats["internet_error"]:
                print(f"Internet Error: {network_stats['internet_error']}")

            log_stats(network_stats)
            check_network_alerts(network_stats)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped network diagnostics.")

def run_combined_monitor() -> None:
    """Run both system and network monitoring."""
    print("\nRunning combined diagnostics...")
    print("Press Ctrl+C to stop.\n")

    alert_counts = {
        "cpu_percent": 0,
        "memory_percent": 0,
        "disk_percent": 0,
    }

    try:
        while True:
            stats = get_system_stats()
            gateway_ip = get_default_gateway()

            if gateway_ip is None:
                print("Could not detect default gateway.")
                return

            print(f"Detected default gateway: {gateway_ip}")

            network_stats = get_network_stats(gateway_ip, PING_TARGET)

            print_stats(stats)

            print(
                f"[NETWORK] "
                f"Gateway Reachable: {network_stats['gateway_reachable']} | "
                f"Gateway Latency: {network_stats['gateway_latency_ms']} ms | "
                f"Internet Reachable: {network_stats['internet_reachable']} | "
                f"Internet Latency: {network_stats['internet_latency_ms']} ms"
            )

            if network_stats["gateway_error"]:
                print(f"Gateway Error: {network_stats['gateway_error']}")

            if network_stats["internet_error"]:
                print(f"Internet Error: {network_stats['internet_error']}")

            combined_stats = {**stats, **network_stats}
            log_stats(combined_stats)

            check_thresholds(stats, alert_counts)
            check_network_alerts(network_stats)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped combined diagnostics.")

def main() -> None:
    """Display a menu and let the user choose what to run."""
    print("-== System Monitoring Tool ==-")
    print("1. Run CPU / RAM / Disk diagnostics")
    print("2. Run network diagnostics")
    print("3. Run both")
    print("4. Exit")

    choice = input('Enter your choice (1-4): ').strip()

    if choice == "1":
        run_system_monitor()
    elif choice == "2":
        run_network_monitor()
    elif choice == "3":
        run_combined_monitor()
    elif choice == "4":
        print("Exiting program.")
    else:
        print("Invalid choice. Please run the program again.")

if __name__ == '__main__':
    main()