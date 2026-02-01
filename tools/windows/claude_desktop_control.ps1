# Claude Desktop Controller for Windows
# Usage from WSL: powershell.exe -ExecutionPolicy Bypass -File claude_desktop_control.ps1 -Action <action> [-Message "text"]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("focus", "send", "status")]
    [string]$Action,

    [string]$Message = ""
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
}
"@

function Find-ClaudeWindow {
    $claudeHandle = [IntPtr]::Zero
    $callback = [Win32+EnumWindowsProc]{
        param($hwnd, $lparam)
        if ([Win32]::IsWindowVisible($hwnd)) {
            $sb = New-Object System.Text.StringBuilder 256
            [Win32]::GetWindowText($hwnd, $sb, 256) | Out-Null
            $title = $sb.ToString()
            # Match exact "Claude" window (not browser tabs)
            if ($title -eq "Claude") {
                $script:claudeHandle = $hwnd
                return $false  # Stop enumeration
            }
        }
        return $true
    }
    [Win32]::EnumWindows($callback, [IntPtr]::Zero) | Out-Null
    return $script:claudeHandle
}

function Focus-Claude {
    $hwnd = Find-ClaudeWindow
    if ($hwnd -eq [IntPtr]::Zero) {
        Write-Host "ERROR: Claude Desktop window not found"
        return $false
    }
    $result = [Win32]::SetForegroundWindow($hwnd)
    if ($result) {
        Write-Host "SUCCESS: Claude Desktop focused"
        Start-Sleep -Milliseconds 300
    }
    return $result
}

function Send-ToClause {
    param([string]$Text)

    if (-not (Focus-Claude)) {
        return $false
    }

    Start-Sleep -Milliseconds 500

    # Type the message
    [System.Windows.Forms.SendKeys]::SendWait($Text)
    Start-Sleep -Milliseconds 200

    # Press Enter to send
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

    Write-Host "SUCCESS: Message sent to Claude Desktop"
    return $true
}

function Get-ClaudeStatus {
    $hwnd = Find-ClaudeWindow
    if ($hwnd -eq [IntPtr]::Zero) {
        Write-Host "STATUS: Claude Desktop NOT running or window not found"
        return $false
    }
    Write-Host "STATUS: Claude Desktop is running (Handle: $hwnd)"
    return $true
}

# Main execution
switch ($Action) {
    "focus" {
        Focus-Claude
    }
    "send" {
        if ([string]::IsNullOrEmpty($Message)) {
            Write-Host "ERROR: -Message parameter required for send action"
            exit 1
        }
        Send-ToClause -Text $Message
    }
    "status" {
        Get-ClaudeStatus
    }
}
