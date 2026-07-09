# Process Plugin

The **Process Plugin** provides process management capabilities for Cipher v2. It is intended to power system-monitoring features and structured process-management commands.

---

## Features

- List running processes
- Search processes by name
- View detailed process information
- Terminate a process
- Force kill a process
- Retrieve CPU and memory usage

---

## Planned Voice Commands

Examples:

- show running processes
- list running applications
- find the Firefox process
- show CPU usage
- show memory usage
- terminate process 1234
- kill Firefox

These commands will be interpreted by Cipher's structured system-intent pipeline before invoking the plugin.

---

## Public Methods

### Process Listing

```python
list_processes()
```

Returns a list of running processes including:

- PID
- Process name
- Username
- Status
- CPU usage
- Memory usage

---

### Search

```python
search("python")
```

Returns all matching processes.

---

### Process Information

```python
process_info(1234)
```

Returns information including:

- PID
- Name
- Status
- Executable path
- Working directory
- Thread count
- CPU usage
- Memory usage

---

### Terminate

Gracefully terminate:

```python
terminate(pid)
```

Force kill:

```python
kill(pid)
```

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

The plugin may report errors when:

- the target process no longer exists
- permission is denied
- the process cannot be terminated
- `psutil` is unavailable

All errors are also written to Cipher's logging system.

---

## Security Notes

- Process termination should normally be confirmed by higher-level assistant logic before execution.
- Killing privileged or system-critical processes may require elevated permissions and can affect system stability.
- The plugin itself performs process operations only when explicitly invoked.

---

## Future Enhancements

Planned capabilities include:

- Process tree visualization
- Live process monitoring
- Resource usage history
- Automatic hung-process detection
- Startup application management
- Service (systemd) management
- Priority (nice) adjustment
- CPU affinity control
- Memory leak detection
- AI-powered process recommendations

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.