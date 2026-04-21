from config import LATENCY_WARNING_MS, LATENCY_CRITICAL_MS
from logger_util import log_alert

def check_network_alerts(network_stats: dict) -> None:
    """Check network conditions and alert if there are problems"""

    if not network_stats['gateway_reachable']:
        message = 'ALERT: Gateway is unreachable.'
        print(message)
        log_alert(message)

    if not network_stats['internet_reachable']:
        message = "ALERT: Internet target is unreachable."
        print(message)
        log_alert(message)

    gateway_latency = network_stats['gateway_latency_ms']
    internet_latency = network_stats['internet_latency_ms']

    if gateway_latency is not None:
        if gateway_latency >= LATENCY_CRITICAL_MS:
            message = f"CRITICAL: Gateway latency is {gateway_latency} ms."
            print(message)
            log_alert(message)
        elif gateway_latency >= LATENCY_WARNING_MS:
            message = f"WARNING: Gateway latency is {gateway_latency} ms."
            print(message)
            log_alert(message)

    if internet_latency is not None:
        if internet_latency >= LATENCY_CRITICAL_MS:
            message = f"CRITICAL: Internet latency is {internet_latency} ms."
            print(message)
            log_alert(message)
        elif internet_latency >= LATENCY_WARNING_MS:
            message = f"WARNING: Internet latency is {internet_latency} ms."
            print(message)
            log_alert(message)