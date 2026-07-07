import platform
import time

import psutil


class SystemMonitor:

    def __init__(self):

        self.boot_time = psutil.boot_time()

    # --------------------------------------------------
    # CPU
    # --------------------------------------------------

    def cpu(self):

        return {
            "percent": psutil.cpu_percent(interval=None),
            "cores": psutil.cpu_count(logical=True),
        }

    # --------------------------------------------------
    # RAM
    # --------------------------------------------------

    def ram(self):

        ram = psutil.virtual_memory()

        return {
            "percent": ram.percent,
            "used_gb": round(ram.used / 1024**3, 1),
            "total_gb": round(ram.total / 1024**3, 1),
            "available_gb": round(ram.available / 1024**3, 1),
        }

    # --------------------------------------------------
    # Disk
    # --------------------------------------------------

    def disk(self):

        disk = psutil.disk_usage("/")

        return {
            "percent": disk.percent,
            "used_gb": round(disk.used / 1024**3, 1),
            "total_gb": round(disk.total / 1024**3, 1),
            "free_gb": round(disk.free / 1024**3, 1),
        }

    # --------------------------------------------------
    # Battery
    # --------------------------------------------------

    def battery(self):

        battery = psutil.sensors_battery()

        if battery is None:

            return {
                "available": False,
            }

        return {
            "available": True,
            "percent": battery.percent,
            "charging": battery.power_plugged,
            "seconds_left": battery.secsleft,
        }

    # --------------------------------------------------
    # Network
    # --------------------------------------------------

    def network(self):

        net = psutil.net_io_counters()

        return {
            "sent_mb": round(net.bytes_sent / 1024 / 1024, 2),
            "received_mb": round(net.bytes_recv / 1024 / 1024, 2),
        }

    # --------------------------------------------------
    # System
    # --------------------------------------------------

    def system(self):

        return {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    # --------------------------------------------------
    # Uptime
    # --------------------------------------------------

    def uptime(self):

        seconds = int(time.time() - self.boot_time)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        return {
            "seconds": seconds,
            "text": f"{hours}h {minutes}m",
        }


system_monitor = SystemMonitor()