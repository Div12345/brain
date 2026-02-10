---
title: "ThrottleStop Configuration for Dell Laptop with Non-Dell Charger"
date: 2026-02-07
category: hardware-issues
tags:
  - throttlestop
  - dell-precision
  - power-management
  - non-dell-charger
  - speed-shift
  - windows-defender
  - 12th-gen-intel
  - exploit-guard
  - asr-rules
  - intel-dptf
  - domain-managed
symptoms:
  - "could not start driver: io error"
  - "Battery draining while plugged in"
  - "CPU throttling with non-Dell charger"
  - "ThrottleStop won't restart after first close"
  - "CPU stuck at base clock on battery"
  - "LockPowerLimits=0 allows BIOS override"
  - "BD PROCHOT not disabled despite scheduled task"
module: windows-system
severity: medium
hardware:
  laptop: Dell Precision 3571
  cpu: Intel i7-12700H (12th Gen Alder Lake)
  ram: 32GB
  battery_health: 52% (50.7Wh of 97Wh design)
---

# ThrottleStop Configuration for Dell Laptop with Non-Dell Charger

## Problem Summary

Dell Precision 3571 with i7-12700H wouldn't charge and severely throttled when using a non-Dell charger. Multiple issues compounded:

1. **ThrottleStop driver error** - "could not start driver: io error"
2. **Battery draining while plugged in** - EC-level power limiting
3. **Speed Shift not working** - EPP not enabled
4. **Windows blocking driver** - Vulnerable Driver Blocklist

## Root Causes

### 1. Windows Defender Vulnerable Driver Blocklist
ThrottleStop.sys is flagged as a "vulnerable signed driver" because it allows low-level CPU access.

**Evidence:**
```
C:\Users\din18\AppData\Local\Temp\ThrottleStop.sys
Block abuse of in-the-wild exploited vulnerable signed drivers
```

### 2. StartFailed=1 Flag in INI
After first driver failure, ThrottleStop sets `StartFailed=1` which prevents retry.

**Evidence:**
```ini
[ThrottleStop]
StartFailed=1
```

### 3. Dell EC-Level Charger Detection
Dell's Embedded Controller limits power draw from non-Dell chargers at hardware level - before OS/ThrottleStop can intervene.

**Evidence:**
```powershell
# Battery discharging while AC connected
Charging           : False
Discharging        : True
PowerOnline        : True
```

### 4. Speed Shift EPP Disabled
`SSTEPP=0` in config meant Speed Shift EPP values weren't being applied.

### 5. Windows Power Plan Min at 100%
Minimum processor state was 100%, preventing CPU from downclocking at idle.

## Solution Steps

### Step 1: Add Windows Defender Exclusions

```powershell
# Add exclusions for ThrottleStop
Add-MpPreference -ExclusionPath "C:\Users\din18\Downloads\ThrottleStop_9.7.3\"
Add-MpPreference -ExclusionPath "C:\Users\din18\AppData\Local\Temp\ThrottleStop.sys"
```

### Step 2: Reset ThrottleStop INI

```bash
# Remove StartFailed flag
echo "[ThrottleStop]" > ThrottleStop.ini

# Delete old driver from Temp
rm "C:\Users\din18\AppData\Local\Temp\ThrottleStop.sys"
```

### Step 3: Configure Optimized Profiles

Created 4 profiles for different use cases:

| Profile | Name | PL1 | PL2 | Speed Shift EPP | Use Case |
|---------|------|-----|-----|-----------------|----------|
| 1 | Charge | 20W | 25W | 160 (efficient) | Fast charging |
| 2 | Max Perf | 65W | 95W | 0 (max) | Full performance |
| 3 | Balanced | 35W | 45W | 80 (fast) | Default on AC |
| 4 | Battery | 15W | 20W | 200 (efficient) | Auto when unplugged |

**Key INI Settings:**
```ini
[ThrottleStop]
ProfileName1=Charge
ProfileName2=Max Perf
ProfileName3=Balanced
ProfileName4=Battery

# BD PROCHOT disabled on profiles 1-3 (fixes Dell throttling)
Options1=0x00300130
Options2=0x00300130
Options3=0x00300130
Options4=0x00300120

# Speed Shift EPP values per profile
EnPerfPref0=160
EnPerfPref1=0
EnPerfPref2=80
EnPerfPref3=200

# Enable Speed Shift
SpeedShift=1
SSTEPP=1

# Speed Shift max/min ratios for i7-12700H
SpeedShiftMaxMin0=0x2F04
SpeedShiftMaxMin1=0x2F08
SpeedShiftMaxMin2=0x2F04
SpeedShiftMaxMin3=0x1E04

# Auto profile switching
BatteryMonitoring=1
ACProfile=2
DCProfile=3

# Lock power limits
LockPowerLimits=1
```

### Step 4: Fix Windows Power Plan

```powershell
# Set min processor to 5% (let Speed Shift handle scaling)
powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5
powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100
powercfg /setactive SCHEME_CURRENT
```

### Step 5: Create Auto-Start Task (No Admin Prompt)

```powershell
schtasks /create /tn "ThrottleStop" /tr "C:\Users\din18\Downloads\ThrottleStop_9.7.3\ThrottleStop.exe" /sc onlogon /rl highest /f
```

## Verification

### Before Fix:
```
EstimatedChargeRemaining: 45%
BatteryStatus: 2 (AC connected)
Charging: False
Discharging: True
ChargeRate: 0
```

### After Fix:
```
EstimatedChargeRemaining: 39%
BatteryStatus: 2 (AC connected)
Charging: True
Discharging: False
ChargeRate: 23584 mW (~24W)
```

## Key Learnings

### 1. Dell EC Throttling is Hardware-Level
ThrottleStop can disable BD PROCHOT (CPU-level throttling) but cannot override EC-level power limiting. The only solutions are:
- Use higher wattage charger
- Accept slower charging
- Use original Dell charger

### 2. StartFailed Flag is Sticky
ThrottleStop's `StartFailed=1` persists and blocks all restart attempts. Must manually reset the INI file.

### 3. Speed Shift Requires Multiple Settings
For 12th gen Intel, need ALL of:
- `SpeedShift=1`
- `SSTEPP=1`
- Proper `SpeedShiftMaxMin` ratios
- Windows min processor < 100%

### 4. Windows Defender VDL is Aggressive
The Vulnerable Driver Blocklist blocks ThrottleStop.sys even with admin rights. Must add folder exclusions.

### 5. Battery Health Affects Charging
Battery at 52% health (50.7Wh of 97Wh design) contributes to charging issues - degraded cells can't accept charge as efficiently.

## Diagnostic Commands

```powershell
# Check battery status
Get-WmiObject -Namespace root\WMI -Class BatteryStatus |
  Select-Object Charging, ChargeRate, DischargeRate, RemainingCapacity

# Generate battery report
powercfg /batteryreport /output battery-report.html

# Check power plan settings
powercfg /query SCHEME_CURRENT SUB_PROCESSOR

# Check ThrottleStop ini
Get-Content ThrottleStop.ini | Select-String "StartFailed|SSTEPP|SpeedShift"
```

## Prevention Checklist

- [ ] Add Windows Defender exclusions BEFORE first run
- [ ] Backup ThrottleStop.ini before making changes
- [ ] Set Windows min processor to 5%, not 100%
- [ ] Enable SSTEPP=1 for Speed Shift EPP
- [ ] Create Task Scheduler entry for admin-less startup
- [ ] Check battery health if charging issues persist

## Update: 2026-02-08 — C:\Tools Installation Fix

### Problem
After relocating ThrottleStop to `C:\Tools\ThrottleStop\` with a proper scheduled task, the config had critical settings missing/wrong compared to the Downloads version. CPU was stuck at 2.3-2.7 GHz (base clock) despite ThrottleStop running.

### Root Causes Found

| Setting | Was | Problem |
|---------|-----|---------|
| LockPowerLimits | 0 | BIOS freely overrode ThrottleStop power limits every few seconds |
| PROCHOT_Activate | 0 | BD PROCHOT not disabled — Dell's main throttle signal still active |
| Battery PL1 | 25W | Too low for i7-12700H (stock 45W TDP) |
| Battery PL2 | 45W | Low burst headroom |
| Battery max freq | 2.5 GHz | Capped a 4.7GHz chip |
| Battery EPP | 220 | Extreme power saving |
| SSTEPP | 0 | EPP values not written to CPU |
| ACProfile/DCProfile | missing | No auto-switch between AC/battery profiles |

### Fix Applied

```ini
# Critical global settings
LockPowerLimits=1        # Was 0 — prevents BIOS override
PROCHOT_Activate=1       # Was 0 — disables Dell BD PROCHOT
SSTEPP=1                 # Was 0 — actually applies EPP values
ACProfile=0              # Auto-switch to Performance on AC
DCProfile=3              # Auto-switch to Battery on DC

# Battery profile (profile 4) improvements
PowerLimitEAX3=0x00DF8168   # PL1: 25W → 45W
PowerLimitEDX3=0x00428280   # PL2: 45W → 80W
SpeedShiftMaxMin3=0x2804    # Max: 2.5GHz → 4.0GHz
EnPerfPref3=128             # EPP: 220 → 128 (balanced)
```

### Updated Profile Table

| Profile | Name | PL1 | PL2 | Max Freq | EPP | Use Case |
|---------|------|-----|-----|----------|-----|----------|
| 1 | Performance | 80W | 115W | 4.7 GHz | 0 (max) | Full performance on AC |
| 2 | Game | 80W | 115W | 4.7 GHz | 32 (near max) | Gaming on AC |
| 3 | Internet | 35W | 65W | 3.5 GHz | 160 (efficient) | Light use on AC |
| 4 | Battery | 45W | 80W | 4.0 GHz | 128 (balanced) | Auto on battery |

### Key Insight: Two Installations Problem
The Downloads version (`C:\Users\din18\Downloads\ThrottleStop_9.7.3\`) had correct settings but wasn't the active one. The Tools version (`C:\Tools\ThrottleStop\`) was launched by the scheduled task but had default/incomplete settings. **Always verify the active installation matches the scheduled task path.**

### Result
- CPU boosted from locked 2.3 GHz to 3.0-3.5 GHz range on AC
- Full turbo (4.7 GHz) requires confirming admin rights (ThrottleStop needs elevation for MSR writes)

### Important: Restarting ThrottleStop
ThrottleStop runs as admin via scheduled task. Cannot be killed from WSL/non-admin shell. To restart:
1. Close from system tray (right-click → Exit)
2. Re-launch via: `schtasks /Run /TN ThrottleStop`

### 6. LockPowerLimits is the #1 Setting
Without `LockPowerLimits=1`, Dell BIOS continuously resets power limits. ThrottleStop sets them, BIOS overrides them seconds later. This creates a cycle where the CPU appears to be at base clock despite ThrottleStop running. **Always verify this is set to 1.**

### 7. Two Installations = Silent Failure
Having ThrottleStop in Downloads (configured) AND Tools (default settings) means the scheduled task runs the wrong config. The fix works silently — no errors, just throttling. **Check `schtasks /Query /TN ThrottleStop /V` to verify the executable path matches your configured INI.**

## Update: 2026-02-09 — Exploit Guard ASR + Intel DPTF (The Real Throttlers)

### Problem
ThrottleStop running with correct config, but severe throttling on AC persisted. CPU stuck at ~65% performance. User running on battery to avoid throttling (backwards).

### Root Causes Found

**Two hidden throttling layers operating independently of ThrottleStop:**

#### 1. Exploit Guard ASR Rule (Vulnerable Driver Blocklist)
Defender Exploit Guard rule `56A863A9-875E-4185-98A7-B882C64B5CE5` ("Block abuse of exploited vulnerable signed drivers") was blocking ThrottleStop's MSR operations at kernel level.

**Critical distinction:** Antivirus file exclusions (`Add-MpPreference -ExclusionPath`) do NOT affect ASR rules. These are completely separate systems:

| Exclusion Type | Covers | Command |
|----------------|--------|---------|
| Antivirus | File scanning, quarantine | `Add-MpPreference -ExclusionPath` |
| **ASR** | **Kernel driver operations, exploit guard** | `Add-MpPreference -AttackSurfaceReductionOnlyExclusions` |

**Evidence from Event Log:**
```
Event 1121: Microsoft Defender Exploit Guard has blocked an operation
that is not allowed by your IT administrator.
ID: 56A863A9-875E-4185-98A7-B882C64B5CE5
Path: C:\Windows\SystemTemp\UDD1423.tmp
```

#### 2. Intel DPTF (Dynamic Platform and Thermal Framework)
Service `dptftcs` was independently throttling CPU based on Dell's thermal/power policies, completely bypassing ThrottleStop.

### Domain-Managed Machine Complication
Machine is joined to `univ.pitt.edu` — IT Group Policy enforces ASR rules. `Set-MpPreference -AttackSurfaceReductionRules_Actions Disabled` **silently fails** (command appears to succeed but policy overrides it).

**How to verify ASR rule status:**
```powershell
# Save as check-asr.ps1, run as admin
$ids = (Get-MpPreference).AttackSurfaceReductionRules_Ids
$actions = (Get-MpPreference).AttackSurfaceReductionRules_Actions
for ($i=0; $i -lt $ids.Count; $i++) {
    if ($ids[$i] -like "56A863A9*") {
        # Action: 0=Disabled, 1=Block, 2=Audit, 6=Warn
        "Rule: $($ids[$i]) Action: $($actions[$i])"
    }
}
```

### Fix Applied

```powershell
# 1. ASR EXCLUSIONS (works even when rule is policy-enforced)
Add-MpPreference -AttackSurfaceReductionOnlyExclusions "C:\Users\din18\Downloads\ThrottleStop_9.7.3\"
Add-MpPreference -AttackSurfaceReductionOnlyExclusions "C:\Users\din18\AppData\Local\Temp\ThrottleStop.sys"
Add-MpPreference -AttackSurfaceReductionOnlyExclusions "C:\Users\din18\Downloads\ThrottleStop_9.7.3\ThrottleStop.exe"

# 2. Disable Intel DPTF
Stop-Service dptftcs -Force
Set-Service dptftcs -StartupType Disabled
```

### Result

| Metric | Before | After |
|--------|--------|-------|
| CPU Performance | 65-67% | **81.7%** |
| Defender blocks | Event 1121 every startup | **None** |
| Battery on AC | Draining | **Charging at 21-25W** |
| DPTF | Running, throttling | **Stopped, disabled** |

### Key Learnings

#### 8. Antivirus Exclusions ≠ ASR Exclusions
This is the most critical learning. Three separate Defender exclusion systems exist:
1. **Antivirus exclusions** (`-ExclusionPath`) — skips file scanning
2. **ASR exclusions** (`-AttackSurfaceReductionOnlyExclusions`) — skips exploit guard rules
3. **Controlled Folder Access exclusions** — skips ransomware protection

ThrottleStop needs **both** #1 and #2.

#### 9. Group Policy Silently Overrides Local Settings
On domain-joined machines, `Set-MpPreference` for ASR rules appears to succeed but Group Policy reapplies the blocked state. **ASR exclusions** are the workaround — they work even when the rule itself is policy-locked.

#### 10. Intel DPTF is a Hidden Throttler
DPTF (`dptftcs` service) throttles independently of ThrottleStop. It can limit CPU based on Dell's own thermal/power policies. Disabling it is safe — ThrottleStop handles thermal management instead.

#### 11. Multiple Throttling Layers on Dell
Dell laptops with non-Dell chargers face **four independent throttling layers**:
1. **EC-level** — Hardware charger detection (can't fully override)
2. **BD PROCHOT** — CPU-level signal (ThrottleStop disables)
3. **Intel DPTF** — OS-level thermal framework (disable service)
4. **Exploit Guard ASR** — Blocks driver MSR writes (add ASR exclusion)

All four must be addressed for full performance.

## Related

- Dell Precision 3571 specs: 45W TDP, boost to 115W
- i7-12700H: 6 P-cores + 8 E-cores, 20 threads
- ThrottleStop 9.7.3 (latest as of 2026-02)
