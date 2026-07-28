# Bluetooth Plugin

## Overview

The Bluetooth plugin enables Cipher to manage Bluetooth adapters and
devices through the centralized `BluetoothService`.

The plugin itself never communicates directly with BlueZ, `bluetoothctl`,
or operating system Bluetooth APIs. Its responsibilities are limited to:

- Detecting Bluetooth-related commands
- Parsing user requests
- Delegating operations to `BluetoothService`
- Returning formatted responses

This keeps all Bluetooth logic centralized and reusable across Cipher.

---

## Features

- View Bluetooth status
- Enable Bluetooth
- Disable Bluetooth
- Scan nearby devices
- Pair with devices
- Connect to paired devices
- Disconnect devices
- List paired/available devices

---

## Example Commands

### Status

```text
bluetooth
```

```text
bluetooth status
```

---

### Power Control

```text
turn on bluetooth
```

```text
enable bluetooth
```

```text
turn off bluetooth
```

```text
disable bluetooth
```

---

### Device Discovery

```text
scan bluetooth
```

```text
bluetooth devices
```

---

### Pairing

```text
pair bluetooth Sony WH-1000XM5
```

---

### Connection

```text
connect bluetooth Sony WH-1000XM5
```

```text
disconnect bluetooth Sony WH-1000XM5
```

---

## Dependencies

This plugin depends on:

- `services.bluetooth_service`

---

## Required Permissions

- System

---

## Architecture

```text
User
   │
   ▼
Bluetooth Plugin
   │
   ▼
BluetoothService
   │
   ├── BlueZ
   ├── bluetoothctl
   ├── DBus
   └── Platform Bluetooth APIs
```

All adapter management, device discovery, pairing, authentication,
connection handling, and platform-specific implementation should remain
inside `BluetoothService`.

---

## Future Enhancements

Potential future capabilities include:

- Device trust management
- Battery level reporting
- Automatic reconnection
- Bluetooth audio profile selection
- File transfer (OBEX)
- BLE device discovery
- Signal strength display
- Device aliases
- Multi-device management

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**