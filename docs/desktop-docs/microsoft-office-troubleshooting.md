# Microsoft Office - Troubleshooting

This guide provides solutions for common account, licensing, and installation errors associated with Microsoft Office at KU.

## 1. General Support

### Account & Device Lock

- **Inactivity Lock:** KU IT automatically disables any device that has not checked in with the network for 210 days.
- **Resolution:** You must contact the IT Customer Service Center at 785-864-8080 to have a support ticket opened and assigned to your technical support team.

### Unsupported Versions

Ensure you are using a version of Office supported by the university (typically Microsoft 365). Older versions like Office 2013 or 2016 may lack critical security updates or feature compatibility.

## 2. Mac Troubleshooting

### Reactivate Office after Password Change

1. Open any Microsoft product (Word, Excel, etc.).
2. Click **Sign In** at the top left of the application.
3. Log in using your KU Online ID and password via the Single Sign-On (SSO) prompt.

### License Removal Tool

If you experience persistent activation errors or "unlicensed product" messages on a Mac, use the License Removal Tool.

1. Download and open the .pkg file from your Downloads folder.
2. Follow the prompts in the setup wizard and select Install.
3. Once the tool completes the removal, click Close and restart an Office app to sign in fresh.

### Uninstalling Office (Mac)

1. **Applications:** Open Finder > Applications and move all Microsoft apps (Word, Excel, etc.) to the Trash.
2. **Library Cleanup:** Go to ~/Library/Containers and delete folders related to Microsoft (e.g., com.microsoft.Word).
3. **Group Containers:** Go to ~/Library/Group Containers and delete folders starting with UBF8T346G9.
4. **Finalize:** Empty the Trash and restart your Mac.

## 3. Windows Troubleshooting

### Credential Manager

If Office keeps asking for your password, clear the cached credentials:

1. Search for Control Panel and go to User Accounts > Credential Manager.
2. Select **Windows Credentials**.
3. Find any entries starting with MicrosoftOffice16 or SSO_POP_Device and click **Remove**.

### Common Error Codes

- **Error 401 login.ku.edu:** This indicates an incorrect Online ID or password. Double-check your credentials and try again.
- **Error 657rx:** Typically caused by a conflict with your "Work or School" account settings.
  - **Fix:** Go to Settings > Accounts > Access work or school. Find your KU account and click Disconnect. Restart the computer and sign in again.

### Repair or Uninstall (Windows)

1. Search for Control Panel > Programs and Features.
2. Right-click your Microsoft Office product.
3. Select **Change**, then choose **Quick Repair** (faster) or **Online Repair** (more thorough).
4. If repairing fails, select **Uninstall** from the same menu and restart before reinstalling.

## Contact Information

For further assistance, please contact the KU IT Customer Service Center:

- **Email:** itcsc@ku.edu
- **Phone:** 785-864-8080
- **Location:** Price Computing Center, 1001 Sunnyside Ave.
