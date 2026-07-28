# Power Plugin

The **Power Plugin** enables Cipher v2 to safely control Ubuntu power-management features using natural language commands.

---

## Features

- Shutdown the computer
- Restart (Reboot)
- Log out of the current session
- Suspend (Sleep)
- Hibernate
- Lock the screen

---

## Safety

Potentially destructive operations require explicit confirmation.

The following actions require confirmation before execution:

- Shutdown
- Restart
- Logout

Example:

User:
```
shutdown computer
```

Cipher:

```
Shutdown requires confirmation.
Say "shutdown now" or "shutdown confirmed".
```

---

## Supported Commands

### Shutdown

- shutdown
- shutdown computer
- power off
- poweroff
- turn off computer
- switch off

---

### Restart

- restart
- reboot
- restart computer
- reboot computer

---

### Logout

- logout
- log out
- sign out

---

### Suspend

- suspend
- sleep
- sleep computer

---

### Hibernate

- hibernate

---

### Lock Screen

- lock
- lock screen
- lock computer

---

## Returned Result

Successful execution:

```python
{
    "success": True,
    "message": "Shutdown command executed."
}
```

Confirmation required:

```python
{
    "success": False,
    "requires_confirmation": True,
    "action": "shutdown",
    "message": "Shutdown requires confirmation. Say 'shutdown now'."
}
```

Failure:

```python
{
    "success": False,
    "message": "<error message>"
}
```

---

## Dependencies

Uses standard Ubuntu utilities:

- `systemctl`
- `loginctl`
- `gnome-session-quit`

No external Python packages are required.

---

## Future Enhancements

Planned improvements include:

- Scheduled shutdown and restart
- Cancel pending shutdown
- Battery-aware shutdown suggestions
- Wake-on-LAN integration
- Multi-user session handling
- Custom confirmation timeout
- Voice confirmation support
- GUI confirmation dialog
- UPS status awareness
- Power profiles integration

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.