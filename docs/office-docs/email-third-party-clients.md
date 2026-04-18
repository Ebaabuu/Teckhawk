# Email - KU Account Setup on Third Party Email Clients

## Support Policy

KU IT only provides support for **Thunderbird**. All other third-party clients are unsupported. Thunderbird uses IMAP and does not sync contacts or calendars without specific plugins.

## Configuration for Thunderbird

1. Open Thunderbird and go to **Account Settings** > **Add Mail Account**.
2. **Email Address:** Use `username@home.ku.edu` (recommended).
3. **Incoming Server (IMAP):**
   - **Server:** `outlook.office365.com`
   - **Port:** 993
   - **Security:** SSL/TLS
   - **Authentication:** OAuth2
4. **Outgoing Server (SMTP):**
   - **Server:** `smtp.office365.com`
   - **Port:** 587
   - **Security:** STARTTLS
   - **Authentication:** OAuth2

## Folder Sync Fix

If folders are missing, go to **Server Settings** > **Advanced** and deselect **Show only subscribed folders**.
