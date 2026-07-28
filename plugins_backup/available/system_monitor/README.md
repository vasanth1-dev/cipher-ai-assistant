# System Monitor Plugin

The **System Monitor Plugin** provides real-time system resource information for Cipher v2. It is intended to supply monitoring data to the assistant, GUI widgets, dashboards, and automation features.

---

## Features

- CPU utilization
- CPU core count
- Memory (RAM) usage
- Disk usage
- Network I/O statistics
- Battery information (when available)
- System boot time
- System uptime

---

## Planned Voice Commands

Examples:

- show system status
- system monitor
- how much RAM is being used
- CPU usage
- disk usage
- battery status
- network usage
- how long has the computer been running

These requests will be routed through Cipher's structured system-intent pipeline.

---

## Public Methods

### Snapshot

```python
snapshot()
```

Returns a dictionary containing:

- CPU utilization
- CPU count
- Memory statistics
- Disk statistics
- Network statistics
- Boot time
- Uptime
- Battery information (if available)

---

## Example Response

```python
{
    "cpu_percent": 18.4,
    "cpu_count": 8,
    "memory": {
        "total": 16777216000,
        "available": 9158324224,
        "used": 7618891776,
        "percent": 45.4
    },
    "disk": {
        "total": 512110190592,
        "used": 182393438208,
        "free": 329716752384,
        "percent": 35.6
    },
    "network": {
        "bytes_sent": 15233445,
        "bytes_received": 108442332
    },
    "boot_time": "2026-07-08T08:15:10",
    "uptime_seconds": 37621,
    "battery": {
        "percent": 82,
        "plugged": true,
        "seconds_left": -2
    }
}
```

> Battery information is included only on systems that expose battery data.

---

## Dependencies

Python package:

- `psutil`

Install:

```bash
pip install psutil
```

---

## Error Handling

The plugin reports errors when:

- `psutil` is unavailable
- monitoring information cannot be retrieved

All exceptions are also recorded through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Live monitoring stream
- Historical resource graphs
- GPU utilization
- CPU temperature
- Fan speed monitoring
- SMART disk health
- Top resource-consuming processes
- Performance alerts
- Export monitoring data (CSV/JSON)
- GUI dashboard integration
- AI-powered performance recommendations

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.