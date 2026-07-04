import psutil
import platform


class SystemMonitor:

    def cpu(self):
        return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"

    def ram(self):
        ram = psutil.virtual_memory()
        return (
            f"RAM Usage: {ram.percent}% "
            f"({round(ram.used/1024**3,1)} GB / {round(ram.total/1024**3,1)} GB)"
        )

    def disk(self):
        disk = psutil.disk_usage("/")
        return (
            f"Disk Usage: {disk.percent}% "
            f"({round(disk.used/1024**3,1)} GB / {round(disk.total/1024**3,1)} GB)"
        )

    def battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery information not available."

        status = "Charging" if battery.power_plugged else "Not Charging"

        return f"Battery: {battery.percent}% ({status})"

    def network(self):

        net = psutil.net_io_counters()

        return (
            f"Sent: {round(net.bytes_sent/1024/1024,2)} MB\n"
            f"Received: {round(net.bytes_recv/1024/1024,2)} MB"
        )

    def system(self):

        return (
            f"{platform.system()} "
            f"{platform.release()} "
            f"({platform.machine()})"
        )


system_monitor = SystemMonitor()