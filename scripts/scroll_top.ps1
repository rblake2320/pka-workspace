Add-Type -AssemblyName System.Windows.Forms
# Send Ctrl+Home to scroll to top of page
[System.Windows.Forms.SendKeys]::SendWait("^{HOME}")
Start-Sleep -Milliseconds 500
