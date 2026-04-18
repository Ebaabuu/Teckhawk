# KU File Storage: Central (CFS) and Research (ResFS)

## Overview

The University of Kansas provides central file storage solutions for students, faculty, and staff. Stored data is accessible within the KU network or remotely via the KU Anywhere VPN.

## Network Drive Paths

The specific file path depends on the type of storage you are accessing. If you are unsure of your specific path, contact your department support staff.

- **Central File Storage (CFS):** kucfs.ku.edu
- **Research File Storage (ResFS):** resfs.home.ku.edu
- **Enterprise File Storage (EFS):** kuefs.ku.edu

## Access Instructions by Operating System

### Windows

1. **Connect to VPN:** If off-campus, connect to KU Anywhere.
2. **Open File Explorer:** Press Windows Key + E.
3. **Map Network Drive:** Right-click on This PC and select Map network drive...
4. **Enter Path:** Choose a drive letter and enter the folder path (e.g., `\\kucfs.ku.edu\home\`).
5. **Authenticate:** When prompted, use your KU Online ID and password (format: `home\KUOnlineID`).

### Mac (macOS)

1. **Connect to VPN:** If off-campus, connect to KU Anywhere.
2. **Connect to Server:** In Finder, press Command + K or select Go > Connect to Server.
3. **Enter Server Address:** Type the path using the SMB protocol (e.g., `smb://kucfs.ku.edu/home/`).
4. **Authenticate:** Click Connect and enter your KU Online ID and password when prompted.

### Linux

1. **Connect to VPN:** Ensure your KU Anywhere VPN connection is active.
2. **Mount Drive:** Use the mount command with the appropriate CIFS/SMB parameters.
3. **Path Example:** `//kucfs.ku.edu/home/[path]`

Note: Specific mount commands may vary based on your Linux distribution and local permissions.

## Troubleshooting & Support

- **Remote Access:** Accessing these drives from off-campus requires an active KU Anywhere VPN connection.
- **Permissions:** If you receive an "Access Denied" error, verify your credentials or contact your department support to ensure your account has been granted access to the specific directory.
- **Storage Increases:** For information regarding increasing your Research File Storage (ResFS) limits, visit the Research File Storage service page.
