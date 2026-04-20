import os

CPU_THRESHOLD: int = 85
MEMORY_THRESHOLD: int = 80
DISK_THRESHOLD: int = 90

CHECK_INTERVAL: int = 5
CONSECUTIVE_ALERTS_REQUIRED: int = 2

DISK_PATH = "C:\\" if os.name == 'nt' else "/"

LOG_DIR: str = 'logs'
LOG_FILE: str = f"{LOG_DIR}/performance.log"