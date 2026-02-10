"""
CV Death Exploratory Analysis v2
Task 4: Descriptive exploration of mortality in arterial analysis dataset.
Two comparisons: (1) All-cause death vs survivor, (2) CV death vs survivor.
Univariate Mann-Whitney U, no adjustment. Hypothesis-generating only.
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

# ══════════════════════════════════════════════════════════════════════════════
# 1. LOAD & MERGE
# ══════════════════════════════════════════════════════════════════════════════

split = pd.read_csv(f"{BASE}/data/processed/split/train_test_split.csv")
demo = pd.read_csv(f"{BASE}/data/processed/demographics/merged_demographics.csv")
cvd = pd.read_excel(f"{BASE}/Comprehensive Taiwan Data Analysis Zahra.xlsx",
                    sheet_name='CVD related Information')
waveform = pd.read_csv(f"{BASE}/data/processed/targets/foot_calibrated_waveform_extractions.csv")

# Clean CVD sheet (has text header rows)
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

# Group labels
df['group3'] = 'Survivor'
df.loc[df['is_dead'] & ~df['is_cv_death'], 'group3'] = 'Non-CV Death'
df.loc[df['is_cv_death'], 'group3'] = 'CV Death'

df['group2'] = np.where(df['is_dead'], 'Dead', 'Survivor')

n_surv = (df['group3'] == 'Survivor').sum()
n_noncv = (df['group3'] == 'Non-CV Death').sum()
n_cv = (df['group3'] == 'CV Death').sum()
n_dead = df['is_dead'].sum()

print(f"Dataset: {len(df)} subjects")
print(f"  Survivors: {n_surv}")
print(f"  All-cause deaths: {n_dead} (Non-CV: {n_noncv}, CV: {n_cv})")

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEFINE VARIABLES
# ══════════════════════════════════════════════════════════════════════════════

clinical_vars = ['Age', 'Sex', 'height', 'weight', 'SBP', 'DBP', 'MBP', 'PR',
                 'calculated_PWV', 'calc_csbp', 'L_ABI', 'R_ABI',
                 'Smoking', 'hypertension', 'IMT', 'LVM-2D']

waveform_value_vars = ['B_max', 'B_min', 'B_foot', 'A_max', 'A_min', 'A_foot',
                       'C_max', 'C_min', 'C_foot', 'F_max', 'F_min', 'F_foot']

# Derive pulse pressures
for ch in ['B', 'A', 'C', 'F']:
    df[f'{ch}_PP'] = df[f'{ch}_max'] - df[f'{ch}_min']
pp_vars = ['B_PP', 'A_PP', 'C_PP', 'F_PP']

# Derive first-last differences (diastolic decay proxy)
for ch in ['B', 'A', 'C', 'F']:
    df[f'{ch}_decay'] = df[f'{ch}_first'] - df[f'{ch}_last']
decay_vars = ['B_decay', 'A_decay', 'C_decay', 'F_decay']

all_vars = clinical_vars + waveform_value_vars + pp_vars + decay_vars

# Variables known to correlate with age (for caveat column)
age_correlated = {'SBP', 'DBP', 'MBP', 'calculated_PWV', 'calc_csbp', 'IMT', 'LVM-2D',
                  'B_max', 'A_max', 'C_max', 'F_max', 'B_PP', 'A_PP', 'C_PP', 'F_PP'}

# ══════════════════════════════════════════════════════════════════════════════
# 3. DESCRIPTIVE STATS TABLE (3 groups + 2 comparisons)
# ══════════════════════════════════════════════════════════════════════════════

def fmt_mean_sd(data, var):
    vals = data[var].dropna()
    if len(vals) == 0:
        return "—", 0
    if vals.nunique() <= 2:  # binary: show count (%)
        n_pos = vals.sum()
        pct = 100 * vals.mean()
        return f"{int(n_pos)} ({pct:.0f}%)", len(vals)
    else:
        return f"{vals.mean():.1f} ± {vals.std():.1f}", len(vals)

def mwu_test(group_a, group_b, var):
    a = group_a[var].dropna()
    b = group_b[var].dropna()
    if len(a) >= 3 and len(b) >= 3 and a.nunique() > 1 and b.nunique() > 1:
        try:
            _, p = stats.mannwhitneyu(a, b, alternative='two-sided')
            return p
        except:
            return np.nan
    return np.nan

survivors = df[df['group3'] == 'Survivor']
all_dead = df[df['is_dead']]
cv_dead = df[df['is_cv_death']]
noncv_dead = df[df['is_dead'] & ~df['is_cv_death']]

rows = []
for v in all_vars:
    surv_str, surv_n = fmt_mean_sd(survivors, v)
    dead_str, dead_n = fmt_mean_sd(all_dead, v)
    noncv_str, noncv_n = fmt_mean_sd(noncv_dead, v)
    cv_str, cv_n = fmt_mean_sd(cv_dead, v)

    p_dead_vs_surv = mwu_test(all_dead, survivors, v)
    p_cv_vs_surv = mwu_test(cv_dead, survivors, v)

    rows.append({
        'Variable': v,
        f'Survivor (N={n_surv})': surv_str,
        f'All Dead (N={n_dead})': dead_str,
        f'Non-CV Dead (N={n_noncv})': noncv_str,
        f'CV Dead (N={n_cv})': cv_str,
        'p (Dead vs Surv)': f"{p_dead_vs_surv:.3f}" if pd.notna(p_dead_vs_surv) else "—",
        'p (CV vs Surv)': f"{p_cv_vs_surv:.3f}" if pd.notna(p_cv_vs_surv) else "—",
        'Age-correlated?': 'yes' if v in age_correlated else '',
        'p_dead_raw': p_dead_vs_surv,
        'p_cv_raw': p_cv_vs_surv,
    })

table = pd.DataFrame(rows)

# Flag noteworthy
table['Flag'] = ''
for i, row in table.iterrows():
    flags = []
    if pd.notna(row['p_dead_raw']) and row['p_dead_raw'] < 0.05:
        flags.append('D*')
    elif pd.notna(row['p_dead_raw']) and row['p_dead_raw'] < 0.1:
        flags.append('D~')
    if pd.notna(row['p_cv_raw']) and row['p_cv_raw'] < 0.05:
        flags.append('CV*')
    elif pd.notna(row['p_cv_raw']) and row['p_cv_raw'] < 0.1:
        flags.append('CV~')
    table.at[i, 'Flag'] = ' '.join(flags)

# Save clean version (drop raw p columns)
table_clean = table.drop(columns=['p_dead_raw', 'p_cv_raw'])
table_clean.to_csv(f"{OUT}/descriptive_stats_table_v2.csv", index=False)

print("\n══ DESCRIPTIVE STATS TABLE ══")
print(f"Legend: D*=AllDeath p<0.05, D~=AllDeath p<0.1, CV*=CVDeath p<0.05, CV~=CVDeath p<0.1")
print(f"All p-values: Mann-Whitney U, two-sided, UNADJUSTED\n")

flagged = table[table['Flag'] != '']
for _, row in flagged.iterrows():
    age_note = " [age-correlated]" if row['Age-correlated?'] == 'yes' else ""
    print(f"  {row['Variable']:20s}  Dead vs Surv: p={row['p (Dead vs Surv)']:>6s}  "
          f"CV vs Surv: p={row['p (CV vs Surv)']:>6s}  {row['Flag']}{age_note}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. BOX PLOTS — Key variables, 3 groups
# ══════════════════════════════════════════════════════════════════════════════

plot_vars = ['Age', 'SBP', 'DBP', 'MBP', 'PR', 'calculated_PWV', 'calc_csbp',
             'L_ABI', 'R_ABI', 'IMT', 'LVM-2D', 'B_PP', 'A_PP', 'C_PP', 'F_PP',
             'B_max', 'B_decay', 'A_decay', 'C_decay', 'F_decay']

fig, axes = plt.subplots(5, 4, figsize=(20, 22))
fig.suptitle('Clinical & Waveform Variables by Mortality Group\n'
             f'Survivor N={n_surv} | Non-CV Death N={n_noncv} | CV Death N={n_cv}\n'
             'Black dots = individual CV death subjects',
             fontsize=14, fontweight='bold', y=0.98)

colors = {'Survivor': '#66BB6A', 'Non-CV Death': '#FFA726', 'CV Death': '#EF5350'}
order = ['Survivor', 'Non-CV Death', 'CV Death']

for idx, var in enumerate(plot_vars):
    ax = axes[idx // 4, idx % 4]
    data_plot = df[['group3', var]].dropna()
    if len(data_plot) > 0:
        sns.boxplot(data=data_plot, x='group3', y=var, order=order,
                    palette=colors, ax=ax, fliersize=2, linewidth=0.8)
        # Overlay individual CV death points
        cv_data = data_plot[data_plot['group3'] == 'CV Death']
        if len(cv_data) > 0:
            ax.scatter([2]*len(cv_data), cv_data[var], color='black', s=50,
                       zorder=5, edgecolors='white', linewidth=0.8)

        # Add p-value annotations
        p_row = table[table['Variable'] == var].iloc[0]
        p_dead = p_row['p_dead_raw']
        p_cv = p_row['p_cv_raw']
        annot_parts = []
        if pd.notna(p_dead) and p_dead < 0.1:
            annot_parts.append(f"D p={p_dead:.3f}")
        if pd.notna(p_cv) and p_cv < 0.1:
            annot_parts.append(f"CV p={p_cv:.3f}")
        if annot_parts:
            ax.set_title(f"{var}\n{' | '.join(annot_parts)}", fontsize=9, color='red')
        else:
            ax.set_title(var, fontsize=10)
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=25, labelsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(f"{OUT}/boxplots_v2.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ Box plots saved")

# ══════════════════════════════════════════════════════════════════════════════
# 5. WAVEFORM HEATMAP (Z-scored group means)
# ══════════════════════════════════════════════════════════════════════════════

wf_cols = waveform_value_vars + pp_vars + decay_vars
wf_data = df[wf_cols + ['group3']].copy()
for c in wf_cols:
    vals = wf_data[c].dropna()
    if len(vals) > 0 and vals.std() > 0:
        wf_data[c] = (wf_data[c] - vals.mean()) / vals.std()

group_means = wf_data.groupby('group3')[wf_cols].mean().loc[order]

fig, ax = plt.subplots(figsize=(20, 4.5))
sns.heatmap(group_means, cmap='RdBu_r', center=0, ax=ax, annot=True, fmt='.2f',
            linewidths=0.5, cbar_kws={'label': 'Z-score (vs population mean)'})
ax.set_title('Waveform Features by Mortality Group (Z-scored)\n'
             'Red = above population mean | Blue = below',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{OUT}/heatmap_v2.png", dpi=150, bbox_inches='tight')
plt.close()
print("✓ Waveform heatmap saved")

# ══════════════════════════════════════════════════════════════════════════════
# 6. CV DEATH INDIVIDUAL PROFILES (percentile radar)
# ══════════════════════════════════════════════════════════════════════════════

profile_vars = ['Age', 'SBP', 'calc_csbp', 'calculated_PWV', 'IMT', 'LVM-2D',
                'B_PP', 'A_PP', 'B_decay', 'A_decay']

cv_subjects = df[df['is_cv_death']].sort_values('subject_id')

# Percentile table
pct_rows = []
for _, row in cv_subjects.iterrows():
    sid = int(row['subject_id'])
    pct_row = {'Subject': sid}
    for v in profile_vars:
        val = row[v]
        if pd.notna(val):
            pct = stats.percentileofscore(df[v].dropna(), val)
            pct_row[f'{v}_val'] = round(val, 2)
            pct_row[f'{v}_pct'] = round(pct, 0)
        else:
            pct_row[f'{v}_val'] = np.nan
            pct_row[f'{v}_pct'] = np.nan
    pct_rows.append(pct_row)

pct_df = pd.DataFrame(pct_rows)
pct_df.to_csv(f"{OUT}/cv_death_percentile_profiles.csv", index=False)

# Print clean profiles
print("\n══ CV DEATH INDIVIDUAL PROFILES ══")
print(f"{'Subject':>8s}", end='')
for v in profile_vars:
    print(f"  {v:>12s}", end='')
print()
print("-" * (8 + len(profile_vars) * 14))

for _, row in cv_subjects.iterrows():
    sid = int(row['subject_id'])
    print(f"{sid:>8d}", end='')
    for v in profile_vars:
        val = row[v]
        if pd.notna(val):
            pct = stats.percentileofscore(df[v].dropna(), val)
            flag = "!!" if pct > 90 or pct < 10 else "  "
            print(f"  {val:>7.1f} P{pct:>2.0f}{flag}", end='')
        else:
            print(f"  {'—':>12s}", end='')
    print()
print("\n!! = extreme (>90th or <10th percentile)")

# ══════════════════════════════════════════════════════════════════════════════
# 7. SCATTER: Age vs LVM-2D colored by group
# ══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

scatter_pairs = [('Age', 'LVM-2D'), ('Age', 'calculated_PWV'), ('calculated_PWV', 'LVM-2D')]

for ax, (xvar, yvar) in zip(axes, scatter_pairs):
    for g, color in colors.items():
        gdata = df[df['group3'] == g]
        alpha = 0.3 if g == 'Survivor' else 0.8
        size = 20 if g == 'Survivor' else 60
        ax.scatter(gdata[xvar], gdata[yvar], c=color, alpha=alpha, s=size,
                   label=g, edgecolors='white', linewidth=0.3)
    # Label CV death subjects
    for _, row in cv_subjects.iterrows():
        if pd.notna(row[xvar]) and pd.notna(row[yvar]):
            ax.annotate(str(int(row['subject_id'])),
                        (row[xvar], row[yvar]),
                        fontsize=7, fontweight='bold',
                        xytext=(4, 4), textcoords='offset points')
    ax.set_xlabel(xvar)
    ax.set_ylabel(yvar)
    ax.legend(fontsize=8)

fig.suptitle('Key Variable Relationships by Mortality Group\nCV Death subjects labeled by ID',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{OUT}/scatter_pairs_v2.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ Scatter plots saved")

# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  FINAL SUMMARY — CV Death Exploratory Analysis")
print("=" * 70)
print(f"""
  Dataset: {len(df)} subjects (modeling subset with CVD outcome data)
  Groups: Survivor={n_surv}, Non-CV Death={n_noncv}, CV Death={n_cv}

  Method: Univariate Mann-Whitney U (two-sided, unadjusted)
  Caveat: No adjustment for age, sex, or multiple comparisons.
          Variables marked 'age-correlated' may be confounded.

  COMPARISON 1: All-Cause Death (N={n_dead}) vs Survivor (N={n_surv})
""")

dead_flagged = table[(table['p_dead_raw'].notna()) & (table['p_dead_raw'] < 0.1)]
for _, r in dead_flagged.iterrows():
    age_note = " [age-corr]" if r['Age-correlated?'] == 'yes' else ""
    print(f"    {r['Variable']:20s}  p={r['p (Dead vs Surv)']}{age_note}")

print(f"""
  COMPARISON 2: CV Death (N={n_cv}) vs Survivor (N={n_surv})
""")

cv_flagged = table[(table['p_cv_raw'].notna()) & (table['p_cv_raw'] < 0.1)]
for _, r in cv_flagged.iterrows():
    age_note = " [age-corr]" if r['Age-correlated?'] == 'yes' else ""
    print(f"    {r['Variable']:20s}  p={r['p (CV vs Surv)']}{age_note}")

print(f"""
  Notable individual: Subject 608 — age 40, all values extremely low
  (SBP 4th pct, PWV 2nd pct, IMT 2nd pct). Possible different mechanism.

  Outputs: {OUT}/
    descriptive_stats_table_v2.csv
    boxplots_v2.png
    heatmap_v2.png
    scatter_pairs_v2.png
    cv_death_percentile_profiles.csv
""")
print("=" * 70)
