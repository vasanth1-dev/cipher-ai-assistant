# Terminal Plugin

## Overview

The Terminal plugin enables Cipher to execute terminal commands through
the centralized `TerminalService`.

The plugin **does not execute shell commands directly**. Its
responsibilities are limited to:

- Detecting terminal-related commands
- Extracting the command to execute
- Delegating execution to `TerminalService`
- Returning the execution result

Keeping execution inside `TerminalService` allows Cipher to implement
logging, permissions, sandboxing, auditing, and platform-specific
behavior in a single location.

---

## Features

- Execute shell commands
- Execute Bash commands
- Natural language terminal commands
- Centralized command execution
- Safe service-based architecture

---

## Example Commands

### Execute Commands

```text
terminal ls -la
```

```text
terminal pwd
```

```text
run command df -h
```

```text
execute python3 --version
```

```text
execute command free -h
```

```text
shell whoami
```

```text
bash uname -a
```

---

## Dependencies

This plugin depends on:

- `services.terminal_service`

---

## Required Permissions

- Shell
- System

---

## Architecture

```text
User
   │
   ▼
Terminal Plugin
   │
   ▼
TerminalService
   │
   ▼
Shell / Operating System
```

All command validation, execution policy, environment handling, timeout
management, logging, and platform-specific implementation should remain
inside `TerminalService`.

---

## Security Notes

The Terminal plugin should never execute commands directly.

`TerminalService` is responsible for:

- Permission checks
- Command allow/block lists
- Timeout handling
- Output capture
- Error handling
- Audit logging

This design keeps command execution centralized and easier to secure.

---

## Future Enhancements

Potential future capabilities include:

- Interactive terminal sessions
- Streaming command output
- Command history
- Saved command aliases
- Background jobs
- SSH execution
- Remote server management
- AI-assisted command suggestions
- Command confirmation for dangerous operations

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**