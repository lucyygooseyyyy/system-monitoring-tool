import platform
import subprocess
import time


def ping_host(host: str) -> dict:
    """Ping a host once and return success/failure plus latency."""
    system_name = platform.system().lower()

    if system_name == "windows":
        command = ["ping", "-n", "1", host]
    else:
        command = ["ping", "-c", "1", host]

    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=3
        )

        end_time = time.time()
        latency_ms = round((end_time - start_time) * 1000, 2)

        success = result.returncode == 0

        return {
            "host": host,
            "success": success,
            "latency_ms": latency_ms if success else None,
            "error": None
        }

    except subprocess.TimeoutExpired:
        return {
            "host": host,
            "success": False,
            "latency_ms": None,
            "error": "Ping timed out"
        }

    except Exception as e:
        return {
            "host": host,
            "success": False,
            "latency_ms": None,
            "error": str(e)
        }


def get_network_stats(gateway_ip: str, internet_target: str) -> dict:
    """Check gateway and internet connectivity."""
    gateway_result = ping_host(gateway_ip)
    internet_result = ping_host(internet_target)

    return {
        "gateway_reachable": gateway_result["success"],
        "gateway_latency_ms": gateway_result["latency_ms"],
        "gateway_error": gateway_result["error"],
        "internet_reachable": internet_result["success"],
        "internet_latency_ms": internet_result["latency_ms"],
        "internet_error": internet_result["error"],
    }