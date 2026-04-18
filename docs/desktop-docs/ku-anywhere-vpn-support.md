# KU Anywhere (VPN) - Support

## Summary

Users may experience trouble connecting to the VPN for various reasons. The KU IT Customer Service Center has identified common solutions for the most frequent issues.

## Pre-Troubleshooting Checklist

Before attempting deeper fixes, verify these basic system settings on your device:

- **Date & Time:** Ensure your device is set to the correct local time.
- **Time Zone:** Confirm the time zone is accurate for your current location.
- **Authentication:** Verify your password and Duo method are working by logging into a private browser window and accessing a KU service.

## Troubleshooting: macOS

If you are having connectivity issues on a Mac, follow these steps to reset the application:

1. **Clear Preferences:**
   - Open **Finder** and select the **Applications** folder.
   - Navigate to **Cisco** > **Cisco Secure Client**.
   - Close the application and attempt to clear preferences (requires navigating to local app data folders).
2. **Terminal Verification:**
   - Open **Launchpad** and search for **Terminal**.
   - Advanced users can use terminal commands to verify if the VPN service is running or blocked.

## Troubleshooting: Windows

Most Windows connection issues are resolved by clearing the application's local cache:

1. **Clear Cisco Cache:**
   - Close the **Cisco Secure Client**.
   - Open the **Start menu** and type `%localappdata%`.
   - Select the **File Location** option that appears.
   - Open the **Cisco** folder and delete the preferences files within the Secure Client folder.
2. **Restart Service:** Reboot your computer to ensure all background Cisco services reset.

## Specific Error Resolutions

| Error/Issue | Resolution |
| :--- | :--- |
| **"Activating Adapter fails"** | This is often caused by **WebRoot** antivirus. Temporarily disable WebRoot to allow the connection. |
| **"Another user is logged in"** | Restart the computer or have other users log out completely before connecting. |
| **No Specific Error Message** | Change your **VPN Entitlement** at myidentity.ku.edu, then wait 2 minutes and try again. |
| **Domain Typos** | Ensure the server address is exactly `kuanywhere.ku.edu`. |

## Escalation & Contact

If the issue persists after clearing the cache and verifying credentials:

- **Email:** itcsc@ku.edu
- **Phone:** 785-864-8080
- **Priority:** Mention that you are troubleshooting **KU Anywhere** for faster routing.
