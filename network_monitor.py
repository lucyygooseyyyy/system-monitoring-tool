import psutil
import platform
import subprocess
import time
import re


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

def get_active_interface() -> str | None:
    """Return the name of the first active non-loopback network interface."""
    stats = psutil.net_if_stats()
    addresses = psutil.net_if_addrs()

    for interface_name, interface_stats in stats.items():
        if not interface_stats.isup:
            continue

        for address in addresses.get(interface_name, []):
            if address.family.name == "AF_INET":
                ip = address.address

                if not ip.startswith("127."):
                    return interface_name

    return None


import re
import subprocess


def get_default_gateway() -> str | None:
    """Return the user's default gateway IP on Windows."""
    try:
        result = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=5
        )

        lines = result.stdout.splitlines()

        for line in lines:
            if "Default Gateway" in line:
                parts = line.split(":", 1)

                if len(parts) < 2:
                    continue

                ip = parts[1].strip()

                # Skip blank gateway entries
                if not ip:
                    continue

                # Only accept real IPv4 addresses
                if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
                    return ip

        return None

    except Exception as e:
        print(f"Gateway detection error: {e}")
        return None