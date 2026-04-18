# Microsoft OneDrive - Support (KU)

## Overview

Personal OneDrive accounts are unsupported by KU IT. The following instructions are specifically for KU Microsoft OneDrive for Business accounts to resolve common client issues.

## File Recovery (Version History)

To restore a previous version of a file or recover data:

1. **Access OneDrive Online:** Go to onedrive.ku.edu and sign in.
2. **Locate File:** Click on My Files and navigate to the specific file.
3. **Open Menu:** Click the three dots (...) next to the file name.
4. **Version History:** Select Version History.
5. **Restore:** Click the three dots next to the desired version to either view or restore it.

## Troubleshooting: Mac

### Clear Office Cache

1. **Quit Apps:** Close all Microsoft Office applications.
2. **Open Folder:** In Finder, select Go > Go to Folder...
3. **Enter Path:** Type `~/Library/Containers/com.Microsoft.OsfWebHost/Data/`
4. **Delete Contents:** Delete the contents of this folder. If it does not exist, look for similar folders related to Microsoft Office and clear their data.

### Unable to Verify Account

If you see an "Unable to verify account" error in the Mac client, you must resync via the web:

1. **Login:** Go to onedrive.ku.edu.
2. **Sync:** Click the Sync button at the top of the page.
3. **Open App:** When prompted by your browser, click Open to launch the OneDrive app.
4. **Completion:** Once the sync starts, you can close the "We're syncing your files" notification.

## Troubleshooting: Windows

### Clear Office Cache

1. **Open Run:** Press Windows Key + R.
2. **Enter Path:** Type `%localappdata%\Microsoft\Office\16.0\` and press OK.
3. **Purge Data:** Delete all files and folders within this directory.
4. **Restart:** Restart your computer.
5. **Verify:** Open an Office app to confirm the account/owner name is now correct.

## Uncommon Support Situations

### File Ownership Missing

Follow these steps if a file's "Owner" or "Title" is not displaying correctly:

1. **Login:** Access OneDrive online.
2. **Settings:** Click the Gear icon > OneDrive settings.
3. **Advanced Settings:** Click More settings, then select "Return to the old Site settings page" at the bottom.
4. **Update Info:** Click Title, Description, and Logo.
5. **Confirm Format:** Ensure the Title field is set to Lastname, FirstName.
