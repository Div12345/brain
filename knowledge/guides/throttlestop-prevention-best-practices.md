# ThrottleStop Prevention & Best Practices Guide

## Quick Reference

| Issue | Prevention | Detection | Recovery |
|-------|-----------|-----------|----------|
| WD Blocks .sys | Exclude folder pre-install | Event Viewer logs | Re-add exclusion |
| StartFailed=1 | Backup .ini, run as Admin | Check .ini file | Reset flag in .ini |
| EC Throttles | Use original charger, verify wattage | Clock stuck low | Lower power limits |
| EPP Not Enabled | Check BIOS, verify CPU gen 6+ | EPP shows "N/A" | Set SSTEPP=1 |
| Min State 100% | Query power plan defaults | High idle clocks | Set PROCTHROTTLEMIN=5 |

## Windows Defender Exclusion

```powershell
# Add exclusions BEFORE extracting ThrottleStop
Add-MpPreference -ExclusionPath "C:\ThrottleStop"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\Temp\ThrottleStop.sys"

# Verify exclusions
(Get-MpPreference).ExclusionPath | Where-Object {$_ -like "*Throttle*"}
```

## StartFailed Recovery

```powershell
# Check for StartFailed flag
Get-Content "ThrottleStop.ini" | Select-String "StartFailed"

# Reset if needed
(Get-Content "ThrottleStop.ini") -replace "StartFailed=1", "StartFailed=0" |
  Set-Content "ThrottleStop.ini"
```

## Speed Shift Configuration (12th Gen Intel)

Required settings in ThrottleStop.ini:
```ini
SpeedShift=1          # Enable Speed Shift
SSTEPP=1              # Enable EPP control
EnPerfPref0=128       # Profile 1 EPP (0=max perf, 255=max efficiency)
EnPerfPref1=0         # Profile 2 EPP
EnPerfPref2=80        # Profile 3 EPP
EnPerfPref3=200       # Profile 4 EPP
```

## Windows Power Plan Fix

```powershell
# Set min processor to 5% (allow idle downclocking)
powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5
powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5
powercfg /setactive SCHEME_CURRENT

# Verify
powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN
```

## Auto-Start Without Admin Prompt

```powershell
# Create scheduled task
schtasks /create /tn "ThrottleStop" /tr "C:\Path\To\ThrottleStop.exe" /sc onlogon /rl highest /f
```

## Diagnostic Commands

```powershell
# Battery status (charging/discharging)
Get-WmiObject -Namespace root\WMI -Class BatteryStatus |
  Select-Object Charging, ChargeRate, DischargeRate

# Full battery report
powercfg /batteryreport /output battery-report.html

# CPU info
Get-WmiObject Win32_Processor | Select-Object Name, MaxClockSpeed, CurrentClockSpeed

# Power plan
powercfg /query SCHEME_CURRENT SUB_PROCESSOR
```

## Dell-Specific Notes

- Dell EC throttles non-Dell chargers at hardware level
- BD PROCHOT disable helps but doesn't fix EC limiting
- Charger wattage recommendations:
  - 65W: Light use only, may drain
  - 90W: Should maintain or slow charge
  - 130W+: Full performance possible

## Profile Recommendations

| Profile | PL1 | PL2 | EPP | Use |
|---------|-----|-----|-----|-----|
| Charge | 20W | 25W | 160 | Maximize charging |
| Max Perf | 65W | 95W | 0 | Full power (drains) |
| Balanced | 35W | 45W | 80 | Daily use |
| Battery | 15W | 20W | 200 | Unplugged |
