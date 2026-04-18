# ImageNow - Backup Printer or Scanner Capture Profiles

## Summary

In Perceptive Content (ImageNow), capture profiles for printers and scanners are stored in local configuration files. Backing up these files is essential before software upgrades or when moving to a new workstation to ensure your custom settings are preserved.

## How to Backup Profiles

1. **Log In:** Open and log into the **Perceptive Content** desktop client.
2. **Access Data Folder:**
   - Hold down the **Shift** key on your keyboard.
   - **Right-click** on the top title bar of the Perceptive Content window (this bar typically reads "Perceptive Content – KU-Production").
   - From the hidden menu that appears, select **Explore Application Data folder**.
3. **Copy Configuration Files:**
   - In the folder that opens, locate the XML file named **`inscan`**.
   - Copy this file to a secure backup location (e.g., your OneDrive, V: drive, or a departmental network folder).
   - **Optional:** Check for a second XML file named **`indevice`**. If it exists, copy it to your backup location as well. If it is not present, you may skip this step.

## How to Restore Profiles

1. **Open New Folder:** On the new workstation or after an upgrade, follow the steps above to open the **Application Data folder**.
2. **Restore Files:** Copy your backed-up **`inscan`** (and `indevice` if applicable) files into this folder, overwriting any existing default files.
3. **Restart:** Close and reopen the Perceptive Content client to verify that your capture profiles have been restored.

## Support

For technical assistance with ImageNow or Perceptive Content, contact the IT Customer Service Center at itcsc@ku.edu or 785-864-8080.
