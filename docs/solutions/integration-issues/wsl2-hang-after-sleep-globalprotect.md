---
module: System
date: 2026-02-11
problem_type: integration_issue
component: wsl2
symptoms:
  - "All WSL commands (wsl, wsl -l -v, wsl --shutdown) hang indefinitely after laptop sleep/wake"
  - "4 zombie wsl.exe processes accumulate, each waiting on stuck vmwp.exe"
  - "WslService timeout loop every 3 minutes (Event 7011, 180000ms)"
  - "DCOM permission errors (Event 10016) for domain user account"
  - "vmwp.exe unkillable without admin privileges"
root_cause: architecture_bug
resolution_type: config_fix
severity: critical
recurrence_risk: high
tags: [wsl2, globalprotect, sleep-wake, vsock, hyper-v, vpn, enterprise, networking, tailscale, modern-standby]
environment:
  os: Windows 11 Education 10.0.26100
  wsl_version: 2.7.0.0
  kernel: 6.6.114.1-1
  distro: Ubuntu-24.04
  vpn: Palo Alto GlobalProtect (PANGP Virtual Ethernet Adapter)
  vpn_secondary: Tailscale
  domain: PITT (university-managed)
references:
  - https://github.com/microsoft/WSL/issues/14005
  - https://github.com/microsoft/WSL/issues/12969
  - https://github.com/microsoft/WSL/issues/11002
  - https://live.paloaltonetworks.com/t5/globalprotect-discussions/globalprotect-blocks-the-network-traffic-of-wsl2/td-p/354962
  - https://gist.github.com/danvy/9486bf730371436131cb888ff4c2ceb6
related_docs:
  - 2026-02-07-claude-code-scrolling-wsl-windows-terminal.md
  - 2026-02-07-throttlestop-dell-non-dell-charger-fix.md
---

# WSL2 Hang After Sleep/Wake with GlobalProtect VPN

## Problem

WSL2 becomes completely unresponsive after laptop resumes from sleep (Modern Standby / lid close-open). Every WSL command hangs indefinitely. Multiple zombie `wsl.exe` processes pile up. The only reliable recovery is a full system reboot.

## Environment

- **OS**: Windows 11 Education 10.0.26100 (university-managed, PITT domain)
- **WSL**: 2.7.0.0, Kernel 6.6.114.1-1
- **Distro**: Ubuntu-24.04
- **VPN**: Palo Alto GlobalProtect (PANGP Virtual Ethernet Adapter)
- **Also present**: Tailscale, Hyper-V Default Switch
- **Power**: Modern Standby enabled

## Symptoms

- `wsl`, `wsl -l -v`, `wsl --shutdown` all hang indefinitely
- 4+ zombie `wsl.exe` processes visible in Task Manager
- `vmwp.exe` (VM worker) stuck, unkillable without admin
- `sc query WslService` shows RUNNING (misleading - service is alive but vsock is dead)
- Event Viewer: Event ID 7011 (WslService timeout) repeating every 3 minutes
- Event Viewer: Event ID 10016 (DCOM permission errors)
- Event Viewer: Event ID 1 (Power-Troubleshooter) confirms sleep/wake cycle

## Root Cause Analysis

Three overlapping issues compound to cause the hang:

### 1. WSL2 VSock Zombie State (Primary - Microsoft Bug)

After Windows resumes from Modern Standby, the vsock (virtual socket) communication channel between the Windows host and the WSL2 lightweight VM breaks. The NDIS virtual network adapter fails to restore properly.

- Services report RUNNING but can't communicate with the VM
- Hyper-V logs show the VM boots successfully
- But the vsock handshake between host and guest fails silently
- **This is unfixed by Microsoft** (Issues [#14005](https://github.com/microsoft/WSL/issues/14005), [#12969](https://github.com/microsoft/WSL/issues/12969), [#8696](https://github.com/microsoft/WSL/issues/8696))
- No amount of service restarting fixes kernel-mode vsock state

### 2. GlobalProtect Routing Hijack (Aggravating)

The PANGP Virtual Ethernet Adapter registers with `InterfaceMetric=1` (highest priority), stealing all WSL traffic. GlobalProtect's WFP (Windows Filtering Platform) callout driver intercepts and filters network packets, blocking the WSL2 VM's networking.

### 3. Missing DNS Tunneling (Configuration)

Enterprise firewalls on the university network block WSL's DNS proxy (UDP port 53 from the WSL NAT subnet). The `.wslconfig` had `networkingMode=mirrored` but was missing `dnsTunneling=true`, which bypasses the firewall via Hyper-V hypervisor socket.

### Non-Issue: DCOM Errors

The Event 10016 DCOM permission errors are cosmetic noise. [Microsoft confirms](https://learn.microsoft.com/en-us/troubleshoot/windows-client/application-management/event-10016-logged-when-accessing-dcom) these are by design on domain-joined machines and don't affect WSL.

## Investigation Steps

| Step | Action | Result |
|------|--------|--------|
| 1 | `wsl -l -v` | Hung |
| 2 | `sc query WslService` / `vmcompute` | Both RUNNING (misleading) |
| 3 | Check for AV/VPN processes | Initially missed GlobalProtect (driver, not process) |
| 4 | `wsl --shutdown` | Hung (can't reach stuck WslService) |
| 5 | Force-kill `wsl.exe` processes | Succeeded, but `vmwp.exe` survived |
| 6 | `taskkill /F /PID` on vmwp.exe | Access Denied (system process) |
| 7 | Elevated: `taskkill /F /IM vmwp.exe` | **SUCCESS** |
| 8 | Restart vmcompute + WslService | `wsl -l -v` worked, showed Ubuntu-24.04 Stopped |
| 9 | `wsl -d Ubuntu-24.04` | **Still hung** despite healthy services |
| 10 | Event Log analysis | Found smoking gun: sleep/wake + WslService timeout loop |
| 11 | Network adapter check | Found PANGP (GlobalProtect) + Tailscale adapters |
| 12 | Killed GlobalProtect, disabled adapter | No change - vsock already dead |
| 13 | Full service restart + Hyper-V reset | VM boots per logs, WSL still hangs |
| 14 | Research Microsoft Issues | Confirmed: vsock zombie = reboot required |

**Key Diagnostic Commands:**

```powershell
# Check for stuck processes
powershell "Get-Process wsl*,vmwp,vmmem -EA SilentlyContinue | ft Name,Id,CPU"

# Check event logs for timeout loop
powershell "Get-WinEvent -FilterHashtable @{LogName='System';Id=7011} -MaxEvents 5 | fl TimeCreated,Message"

# Check network adapters
powershell "Get-NetAdapter | ft Name,Status,InterfaceDescription -AutoSize"

# Check sleep/wake events
powershell "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-Power-Troubleshooter'} -MaxEvents 3 | fl TimeCreated,Message"
```

## Immediate Fix

**Only reliable recovery from vsock zombie state: full reboot.**

```powershell
Restart-Computer
```

If you want to attempt recovery without reboot (works ~30% of the time):

```powershell
# Run as Administrator
taskkill /F /IM wslservice.exe
taskkill /F /IM wsl.exe
taskkill /F /IM vmwp.exe
Restart-Service hns -Force
Restart-Service vmcompute -Force
hnsdiag.exe delete all
ipconfig /flushdns
Start-Sleep 3
Start-Service LxssManager
wsl
```

## Prevention

### 1. Fix `.wslconfig`

`C:\Users\<username>\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true

[experimental]
autoMemoryReclaim=disabled
```

- `networkingMode=mirrored` — Bypasses NAT, eliminates GlobalProtect routing conflict
- `dnsTunneling=true` — DNS via Hyper-V socket, bypasses enterprise firewall (critical on managed machines)
- `autoProxy=true` — Mirrors Windows HTTP proxy settings
- `autoMemoryReclaim=disabled` — Prevents resource saver from contributing to sleep issues

Apply: `wsl --shutdown && wsl`

### 2. Pre-Sleep Shutdown (Best Prevention)

Scheduled Task that shuts down WSL before system enters sleep, preventing vsock corruption entirely:

```powershell
# Install pre-sleep shutdown task (run as Admin)
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "--shutdown"

$trigger = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler
$triggerObj = New-CimInstance -CimClass $trigger -ClientOnly
$triggerObj.Enabled = $true
$triggerObj.Subscription = @"
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[Provider[@Name='Microsoft-Windows-Kernel-Power'] and EventID=506]]
    </Select>
  </Query>
</QueryList>
"@

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "WSL-PreSleep-Shutdown" `
    -Action $action -Trigger $triggerObj `
    -Settings $settings -Principal $principal `
    -Description "Shutdown WSL before sleep to prevent vsock corruption" -Force
```

### 3. Post-Wake Recovery Script

Save as `C:\Scripts\wsl-wake-recovery.ps1`:

```powershell
#Requires -RunAsAdministrator
Write-Host "[WSL Recovery] Starting..." -ForegroundColor Cyan

# Kill stuck processes
Get-Process -Name "wsl","wslservice" -EA SilentlyContinue | Stop-Process -Force
Start-Sleep 2

# Reset networking
Restart-Service hns -Force -EA SilentlyContinue
Restart-Service vmcompute -Force -EA SilentlyContinue
Start-Sleep 3

# Clean HNS state
if (Test-Path "C:\Windows\System32\hnsdiag.exe") { hnsdiag.exe delete all | Out-Null }
ipconfig /flushdns | Out-Null

# Restart WSL
Restart-Service LxssManager -Force -EA SilentlyContinue
Start-Sleep 3

# Test
$job = Start-Job { wsl -l -v }
if (Wait-Job $job -Timeout 10) {
    Receive-Job $job
    Write-Host "WSL recovered!" -ForegroundColor Green
} else {
    Stop-Job $job; Remove-Job $job
    Write-Host "Still hung. Reboot required: Restart-Computer" -ForegroundColor Red
}
```

Register as wake-triggered Scheduled Task:

```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\Scripts\wsl-wake-recovery.ps1"

$trigger = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler
$triggerObj = New-CimInstance -CimClass $trigger -ClientOnly
$triggerObj.Enabled = $true
$triggerObj.Subscription = @"
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">
      *[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and EventID=1]]
    </Select>
  </Query>
</QueryList>
"@

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "WSL-PostWake-Recovery" `
    -Action $action -Trigger $triggerObj `
    -Settings $settings -Principal $principal `
    -Description "Recover WSL after system wake" -Force
```

### 4. Interface Metric Fix (VPN Coexistence)

```powershell
# Run as Admin — demote VPN adapters, promote WSL
Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*PANGP*"} |
    Set-NetIPInterface -InterfaceMetric 6000
Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*Tailscale*"} |
    Set-NetIPInterface -InterfaceMetric 5000
Get-NetAdapter | Where-Object {$_.Name -like "*WSL*"} |
    Set-NetIPInterface -InterfaceMetric 1
```

## Quick Recovery Checklist

1. **Run recovery script** as Admin: `powershell -File C:\Scripts\wsl-wake-recovery.ps1`
2. **If still hung**: `Restart-Computer`
3. **After reboot**: Verify `.wslconfig` settings, check `wsl --version`

## Key Learnings

1. **Service status lies** — RUNNING doesn't mean functional. VSock can be zombified while services report healthy.
2. **vmwp.exe requires admin** — VM worker process is system-level, can't be killed from user shell.
3. **Event Logs are the smoking gun** — Event ID 7011 timeout loop + Power-Troubleshooter wake event reveals the correlation.
4. **GlobalProtect hides** — Runs as network driver (PANGP adapter), not visible in process list. Easy to miss.
5. **VSock zombie requires reboot** — No service restart clears corrupted kernel-mode vsock state. Microsoft has not fixed this.
6. **DNS tunneling is essential on enterprise networks** — VPN + firewall double-block NAT-based DNS. `dnsTunneling=true` bypasses both.
7. **Prevention beats recovery** — `wsl --shutdown` before sleep is 95% effective. Post-wake recovery is ~30%.
8. **HNS state persists across service restarts** — Must explicitly clean with `hnsdiag.exe delete all`.
9. **Mirrored networking reduces but doesn't eliminate** — Helps with routing conflicts but doesn't prevent vsock corruption.
10. **Enterprise VPN adapter metrics matter** — GlobalProtect at metric 1 hijacks all traffic including WSL. Demote to 6000.

## Prevention Effectiveness

| Strategy | Effectiveness | Effort |
|----------|---------------|--------|
| Pre-sleep `wsl --shutdown` task | ~95% | Low (one-time setup) |
| `.wslconfig` with dnsTunneling | ~50% reduction | 2 minutes |
| Post-wake recovery script | ~30% avoids reboot | Low (one-time setup) |
| Interface metric management | Prevents routing conflict | Low |
| Manual shutdown before closing lid | ~90% | Requires discipline |

## External References

- [WSL Issue #14005 - VSock zombie after sleep](https://github.com/microsoft/WSL/issues/14005)
- [WSL Issue #12969 - WSL hangs after sleep](https://github.com/microsoft/WSL/issues/12969)
- [WSL Issue #11002 - Mirrored mode + GlobalProtect](https://github.com/microsoft/WSL/issues/11002)
- [GlobalProtect blocks WSL2 traffic - Palo Alto LIVEcommunity](https://live.paloaltonetworks.com/t5/globalprotect-discussions/globalprotect-blocks-the-network-traffic-of-wsl2/td-p/354962)
- [WSL network reset script - GitHub Gist](https://gist.github.com/danvy/9486bf730371436131cb888ff4c2ceb6)
- [DCOM Event 10016 - Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/windows-client/application-management/event-10016-logged-when-accessing-dcom)

## Cross-References

- [Claude Code scrolling in WSL + Windows Terminal](../2026-02-07-claude-code-scrolling-wsl-windows-terminal.md) — WSL/terminal integration
- [ThrottleStop Dell non-Dell charger fix](../2026-02-07-throttlestop-dell-non-dell-charger-fix.md) — Domain-managed laptop, Group Policy, power management
- [Gemini Desktop steering pipeline](../2026-02-05-gemini-desktop-steering-pipeline.md) — Windows Task Scheduler + WSL integration patterns
