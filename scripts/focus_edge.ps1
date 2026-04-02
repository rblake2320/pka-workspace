Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@
$edge = Get-Process msedge | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1
if ($edge) {
    [Win32]::ShowWindow($edge.MainWindowHandle, 3)  # SW_MAXIMIZE
    [Win32]::SetForegroundWindow($edge.MainWindowHandle)
    Write-Output "Focused: $($edge.MainWindowTitle)"
} else {
    Write-Output "No Edge window found"
}
