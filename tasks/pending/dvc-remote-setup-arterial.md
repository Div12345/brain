# DVC Remote Setup for arterial_analysis

**Priority:** Medium (non-blocking for local work)
**Repo:** arterial_analysis
**Prereqs:** DVC init must be done first (separate task)

## Goal
Set up a DVC remote on Pitt OneDrive so data is backed up and recoverable after WSL reformat, and collaborators can pull data with `dvc pull`.

## Steps

### 1. Verify rclone + OneDrive for Business compatibility
- Pitt uses OneDrive for Business (not personal) — different auth flow
- Check: does Pitt IT restrict third-party API access to OneDrive?
- Test: `rclone config` → choose OneDrive → "Microsoft OneDrive for Business" → authenticate
- If blocked: fall back to Google Drive (`gdrive://`) which has native DVC support

### 2. Configure rclone for Pitt OneDrive
```bash
pip install dvc[all]    # includes rclone support
rclone config
# Name: pitt-onedrive
# Storage: onedrive
# Type: business
# Auth: browser-based OAuth
```

### 3. Create DVC remote folder
- Create a dedicated folder on OneDrive for DVC storage (not the repo folder itself)
- Suggested: `OneDrive/Research/arterial_analysis_dvc/`
- This folder stores content-addressed files by hash, not the original directory structure

### 4. Add DVC remote
```bash
cd /mnt/c/.../arterial_analysis
dvc remote add -d pitt rclone://pitt-onedrive/Research/arterial_analysis_dvc
dvc push    # uploads all DVC-tracked data to remote
```

### 5. (Optional) Add Google Drive as backup remote
```bash
dvc remote add gdrive-backup gdrive://<folder-id>
dvc push -r gdrive-backup
```

### 6. Test recovery
```bash
# Delete local DVC cache to simulate fresh clone
rm -rf .dvc/cache
dvc pull    # should restore everything from remote
```

### 7. Document for collaborators
Add to repo README or CLAUDE.md:
```
## Getting the data
1. Install DVC: pip install dvc[all]
2. Configure OneDrive access: rclone config (follow prompts, auth with Pitt account)
3. Pull data: dvc pull
```

## Caveats
- OneDrive for Business token expires — may need periodic re-auth
- Rate limits possible on large initial push (580MB+)
- If Pitt blocks API access, Google Drive is the fallback
- Test `rclone lsd pitt-onedrive:` before configuring DVC to verify access works

## 3-2-1 Backup After Setup
| Copy | Where | Verified by |
|------|-------|-------------|
| 1 | Laptop disk | DVC cache hashes |
| 2 | Pitt OneDrive (DVC remote) | `dvc push` success |
| 3 | Google Drive backup (optional) | `dvc push -r gdrive-backup` |
