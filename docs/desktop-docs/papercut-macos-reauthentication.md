# PaperCut - Re-Authenticating to MFD on macOS

The macOS keychain stores credentials for accounts and other network resources. After a user changes their password, they may be unable to print to campus PaperCut devices without explicitly updating the stored password for the target printer or Multi-Function Device (MFD).

## 1. Updating the Password via Print Queue

In most cases, the password stored in the keychain can be updated directly through the print queue window:

1. Open the print queue that contains the held job.
2. Click the **reload button** located in the queue window.
3. Enter your new password when the system prompts you.

## 2. Removing the Keychain Entry

If the reload method does not work, it may be necessary to explicitly remove the incorrect keychain entry.

1. **Launch Keychain Access:** You can find this via Applications > Utilities or by using Spotlight search.
2. **Search for Printer:** Use the search feature within Keychain Access to find the relevant networked printer by its name.
3. **Delete Entry:** Select the specific queue's password entry in the login keychain.
4. **Confirm:** Choose Delete from the Edit menu to remove the errant entry.
