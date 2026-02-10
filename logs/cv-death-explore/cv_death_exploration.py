"""
CV Death Exploratory Analysis
Task 4: Quick exploration of CV death subjects in arterial analysis dataset.
Descriptive only — hypothesis generating, not testing.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

OUT = "/home/div/brain/logs/cv-death-explore"
BASE = "/mnt/c/Users/din18/OneDrive - University of Pittsburgh/Work/Github/AAA_detection_personal"

# ── 1. Load & Merge ──────────────────────────────────────────────────────────

split = pd.read_csv(f"{BASE}/data/processed/split/train_test_split.csv")
demo = pd.read_csv(f"{BASE}/data/processed/demographics/merged_demographics.csv")
cvd = pd.read_excel(f"{BASE}/Comprehensive Taiwan Data Analysis Zahra.xlsx", sheet_name='CVD related Information')
waveform = pd.read_csv(f"{BASE}/data/processed/targets/foot_calibrated_waveform_extractions.csv")

# Clean CVD sheet
cvd = cvd[cvd['Patient Number'].apply(lambda x: str(x).strip().isdigit())]
cvd['Patient Number'] = cvd['Patient Number'].astype(int)
cvd['is_dead'] = cvd['Death'].astype(float) == 1
cvd['is_cv_death'] = cvd['CV Death'].notna() & (cvd['CV Death'] != 0)

model_ids = set(split['subject_id'])
waveform = waveform.rename(columns={'subID': 'subject_id'})
cvd_slim = cvd[['Patient Number', 'is_dead', 'is_cv_death', 'IMT', 'LVM-2D']].rename(
    columns={'Patient Number': 'subject_id'}
)

df = demo.merge(cvd_slim, on='subject_id', how='inner')
df = df.merge(waveform, on='subject_id', how='inner')
df = df[df['subject_id'].isin(model_ids)]

df['group'] = 'Survivor'
df.loc[df['is_dead'] & ~df['is_cv_death'], 'group'] = 'Non-CV Death'
df.loc[df['is_cv_death'], 'group'] = 'CV Death'

print(f"Dataset: {len(df)} subjects")
print(f"Groups: {df['group'].value_counts().to_dict()}")

# ── 2. Descriptive Statistics Table ──────────────────────────────────────────

clinical_vars = ['Age', 'Sex', 'height', 'weight', 'SBP', 'DBP', 'MBP', 'PR',
                 'calculated_PWV', 'calc_csbp', 'L_ABI', 'R_ABI',
                 'Smoking', 'hypertension', 'IMT', 'LVM-2D']

waveform_vars = ['B_max', 'B_min', 'B_foot', 'A_max', 'A_min', 'A_foot',
                 'C_max', 'C_min', 'C_foot', 'F_max', 'F_min', 'F_foot']

pulse_pressure_vars = []  # we'll derive these

# Derive pulse pressure from waveform channels
for ch in ['B', 'A', 'C', 'F']:
    col = f'{ch}_PP'
    df[col] = df[f'{ch}_max'] - df[f'{ch}_min']
    pulse_pressure_vars.append(col)

all_vars = clinical_vars + waveform_vars + pulse_pressure_vars


def describe_group(data, varlist):
    """Descriptive stats for a group."""
    rows = []
    for v in varlist:
        vals = data[v].dropna()
        if len(vals) == 0:
            rows.append({'variable': v, 'n': 0, 'mean': np.nan, 'std': np.nan, 'median': np.nan})
        elif vals.nunique() <= 2:  # binary
            rows.append({'variable': v, 'n': len(vals), 'mean': vals.mean(), 'std': np.nan, 'median': np.nan})
        else:
            rows.append({'variable': v, 'n': len(vals), 'mean': vals.mean(), 'std': vals.std(),
                         'median': vals.median()})
    return pd.DataFrame(rows)


groups = ['Survivor', 'Non-CV Death', 'CV Death']
desc_tables = {}
for g in groups:
    desc_tables[g] = describe_group(df[df['group'] == g], all_vars)

# Build comparison table
comp = desc_tables['Survivor'][['variable']].copy()
for g in groups:
    t = desc_tables[g]
    comp[f'{g}_n'] = t['n'].values
    comp[f'{g}_mean'] = t['mean'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "—").values
    comp[f'{g}_std'] = t['std'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "—").values

# Simple Mann-Whitney U: CV Death vs Survivor (non-parametric, small N)
pvals = []
for v in all_vars:
    cv_vals = df[df['group'] == 'CV Death'][v].dropna()
    surv_vals = df[df['group'] == 'Survivor'][v].dropna()
    if len(cv_vals) >= 3 and len(surv_vals) >= 3 and cv_vals.nunique() > 1:
        try:
            _, p = stats.mannwhitneyu(cv_vals, surv_vals, alternative='two-sided')
            pvals.append(p)
        except:
            pvals.append(np.nan)
    else:
        pvals.append(np.nan)

comp['MWU_p_CVvsSurv'] = [f"{p:.3f}" if pd.notna(p) else "—" for p in pvals]

# Flag interesting (p < 0.1, NOT claiming significance)
comp['flag'] = ['*' if pd.notna(p) and p < 0.1 else '' for p in pvals]

comp.to_csv(f"{OUT}/descriptive_stats_table.csv", index=False)
print("\n✓ Descriptive stats saved")

# Print flagged variables
flagged = comp[comp['flag'] == '*']
if len(flagged) > 0:
    print(f"\nVariables with MWU p < 0.1 (CV Death vs Survivor):")
    for _, row in flagged.iterrows():
        print(f"  {row['variable']}: p={row['MWU_p_CVvsSurv']}  "
              f"(CV Death mean={row['CV Death_mean']}, Survivor mean={row['Survivor_mean']})")
else:
    print("\nNo variables with p < 0.1")

# ── 3. Box Plots: Clinical Variables by Group ────────────────────────────────

fig, axes = plt.subplots(4, 4, figsize=(18, 16))
fig.suptitle('Clinical & Waveform Variables by Death Group\n(CV Death N=7, Non-CV Death N=27, Survivor N=160)',
             fontsize=14, fontweight='bold')

plot_vars = ['Age', 'SBP', 'DBP', 'MBP', 'PR', 'calculated_PWV', 'calc_csbp',
             'L_ABI', 'R_ABI', 'IMT', 'LVM-2D', 'B_PP', 'A_PP', 'C_PP', 'F_PP', 'B_max']

colors = {'Survivor': '#4CAF50', 'Non-CV Death': '#FF9800', 'CV Death': '#F44336'}
order = ['Survivor', 'Non-CV Death', 'CV Death']

for idx, var in enumerate(plot_vars):
    ax = axes[idx // 4, idx % 4]
    data_plot = df[['group', var]].dropna()
    if len(data_plot) > 0:
        sns.boxplot(data=data_plot, x='group', y=var, order=order,
                    palette=colors, ax=ax, fliersize=3)
        # Overlay CV death individual points
        cv_data = data_plot[data_plot['group'] == 'CV Death']
        if len(cv_data) > 0:
            ax.scatter([2]*len(cv_data), cv_data[var], color='black', s=40,
                       zorder=5, edgecolors='white', linewidth=0.5)
    ax.set_xlabel('')
    ax.set_title(var, fontsize=10)
    ax.tick_params(axis='x', rotation=30, labelsize=8)

plt.tight_layout()
plt.savefig(f"{OUT}/clinical_boxplots.png", dpi=150, bbox_inches='tight')
plt.close()
print("✓ Clinical box plots saved")

# ── 4. Waveform Feature Heatmap ─────────────────────────────────────────────

wf_cols = [c for c in df.columns if any(c.startswith(p) for p in ['B_', 'A_', 'C_', 'F_'])
           and 'success' not in c and 'idx' not in c]

# Z-score normalize within each variable, then show group means
wf_data = df[wf_cols + ['group']].copy()
for c in wf_cols:
    vals = wf_data[c].dropna()
    if len(vals) > 0 and vals.std() > 0:
        wf_data[c] = (wf_data[c] - vals.mean()) / vals.std()

group_means = wf_data.groupby('group')[wf_cols].mean()
group_means = group_means.loc[order]

fig, ax = plt.subplots(figsize=(16, 4))
sns.heatmap(group_means, cmap='RdBu_r', center=0, ax=ax, annot=True, fmt='.2f',
            linewidths=0.5, cbar_kws={'label': 'Z-score (relative to population)'})
ax.set_title('Waveform Features by Group (Z-scored)\nRed = above average, Blue = below average',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{OUT}/waveform_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
print("✓ Waveform heatmap saved")

# ── 5. CV Death Individual Profiles ─────────────────────────────────────────

cv_subjects = df[df['group'] == 'CV Death'][['subject_id'] + clinical_vars + waveform_vars + pulse_pressure_vars]
cv_subjects.to_csv(f"{OUT}/cv_death_individual_profiles.csv", index=False)
print("✓ CV death individual profiles saved")

# Print individual CV death subjects vs population percentiles
print("\n── CV Death Subject Profiles (percentile rank in full population) ──")
for _, row in df[df['group'] == 'CV Death'].iterrows():
    sid = int(row['subject_id'])
    print(f"\n  Subject {sid}:")
    for v in ['Age', 'SBP', 'calc_csbp', 'calculated_PWV', 'IMT', 'B_PP', 'A_PP']:
        val = row[v]
        if pd.notna(val):
            pct = stats.percentileofscore(df[v].dropna(), val)
            marker = " ◄◄" if pct > 90 or pct < 10 else ""
            print(f"    {v}: {val:.1f} (percentile: {pct:.0f}%){marker}")

# ── 6. Summary Stats ────────────────────────────────────────────────────────

print("\n\n══════════════════════════════════════════════")
print("  SUMMARY: CV Death Exploration")
print("══════════════════════════════════════════════")
print(f"  Dataset: {len(df)} subjects (modeling subset with CVD data)")
print(f"  Survivors: {(df['group']=='Survivor').sum()}")
print(f"  Non-CV Deaths: {(df['group']=='Non-CV Death').sum()}")
print(f"  CV Deaths: {(df['group']=='CV Death').sum()}")
print(f"  CV Death IDs: {sorted(df[df['is_cv_death']]['subject_id'].tolist())}")
print(f"\n  Flagged variables (MWU p<0.1): {len(flagged)}")
for _, row in flagged.iterrows():
    print(f"    → {row['variable']}: p={row['MWU_p_CVvsSurv']}")
print(f"\n  Outputs in: {OUT}/")
print("══════════════════════════════════════════════")
