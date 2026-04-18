# Wi-Fi - Troubleshooting (KU)

## Initial Verification

Before proceeding with device-specific steps, verify that your credentials are correct.

- **Password Confirmation:** Ensure you are using your current KU password.
- **Browser Cache vs. Wi-Fi:** Users are often able to log into services via a browser because the password is saved, but Wi-Fi fails because the manual entry is incorrect or forgotten.

## Troubleshooting by Device

### Password Troubleshooting

- **Forget the Network:** If you have recently changed your password, you must "Forget" the Jayhawk or eduroam network and reconnect to trigger a new login prompt.
- **Online ID Format:** Use your standard KU Online ID; do not append @ku.edu unless specifically instructed for eduroam.

### Android & Chromebook

- **CA Certificate:** Set to "Don't validate" or "Use system certificates".
- **Domain:** If prompted for a domain, enter `ku.edu`.
- **Identity:** Enter your KU Online ID.
- **Anonymous Identity:** Leave this field blank.

### iOS (iPhone/iPad)

- **Forget Network:** Go to Settings > Wi-Fi, tap the "i" next to the network, and select Forget This Network.
- **Reset Network Settings:** If connectivity persists, go to Settings > General > Transfer or Reset [Device] > Reset > Reset Network Settings. Note: This will remove all saved Wi-Fi passwords and Bluetooth pairings.

### Mac (macOS)

- **Remove Profiles:** Check System Settings > Privacy & Security > Profiles. Remove any old KU Wi-Fi profiles if they exist.
- **Keychain Access:** Open Keychain Access, search for "Jayhawk," and delete the saved password entry to force a new login.

### Windows

- **Forget Network:** Click the Wi-Fi icon, right-click Jayhawk, and select Forget.
- **Network Reset:** Go to Settings > Network & internet > Advanced network settings > Network reset. This requires a computer restart.
