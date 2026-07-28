# Network Plugin

## Overview

The Network plugin enables Cipher to manage network connectivity through
the centralized `NetworkService`.

The plugin itself never communicates directly with NetworkManager,
`nmcli`, or any operating system networking APIs. Its responsibilities
are limited to:

- Detecting network-related commands
- Parsing user requests
- Delegating operations to `NetworkService`
- Returning formatted responses

This architecture keeps all networking logic centralized and reusable.

---

## Features

- View network status
- View Wi-Fi status
- Scan available Wi-Fi networks
- Connect to a Wi-Fi network
- Disconnect from Wi-Fi
- Enable Wi-Fi
- Disable Wi-Fi
- Show IP address

---

## Example Commands

### Network Status

```text
network
```

```text
network status
```

```text
wifi
```

```text
wi-fi
```

---

### Wi-Fi Control

```text
scan wifi
```

```text
enable wifi
```

```text
disable wifi
```

```text
connect wifi HomeNetwork
```

```text
disconnect wifi
```

---

### IP Information

```text
ip address
```

---

## Dependencies

This plugin depends on:

- `services.network_service`

---

## Required Permissions

- Network
- System

---

## Architecture

```text
User
   │
   ▼
Network Plugin
   │
   ▼
NetworkService
   │
   ├── NetworkManager
   ├── nmcli
   ├── System Network APIs
   └── Future Network Providers
```

All platform-specific networking operations, credential handling,
connection management, error recovery, and network discovery should
remain inside `NetworkService`.

---

## Future Enhancements

Potential future capabilities include:

- Saved Wi-Fi profiles
- Ethernet management
- Bluetooth tethering
- VPN management
- Network speed test
- Bandwidth monitoring
- Signal strength reporting
- Network diagnostics
- Automatic reconnection

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**