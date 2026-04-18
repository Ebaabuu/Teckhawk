# Email - POP and IMAP Settings (Uncommon)

## Summary

KU IT **strongly recommends** that email clients be configured to access KU Email using an Exchange/ActiveSync connection. As of September 29, 2022, email clients must support OAuth or OAuth 2.0. All clients except for the official Outlook application are unsupported.

## Exchange Endpoints

- **Exchange endpoint:** `https://outlook.office365.com/EWS/Exchange.asmx`
- **Autodiscover:** `https://autodiscover-s.outlook.com/Autodiscover/Autodiscover.xml`

## Standard Settings

- **Email Address:** `primaryEmail@ku.edu`
- **Username:** `KUOnlineID@home.ku.edu`
- **Password:** Your KU password

## Server Settings

| Setting | POP Settings | IMAP Settings | SMTP Settings (Outgoing) |
| --- | --- | --- | --- |
| **Server Name** | `outlook.office365.com` | `outlook.office365.com` | `smtp.office365.com` |
| **Port** | 995 | 993 | 587 |
| **Encryption** | SSL | SSL | TLS (or STARTTLS) |

## LDAP Connection (KU Address Book)

- **Directory Server:** `whitepages.ku.edu`
- **Port:** 636 (Use SSL)
- **Search Base:** `ou=people,dc=kc,dc=edu`
