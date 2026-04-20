import time

def cpu_stress_test(duration: int = 10) -> None:
    """Create CPU load for a set number of seconds."""
    print(f"Running CPU stress test for {duration} seconds...")
    end_time = time.time() + duration

    while time.time() < end_time:
        sum(i * i for i in range(500000))