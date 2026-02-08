import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import argparse
import os
from pathlib import Path

# Paths
REPO_ROOT = Path("/home/div/AAA_detection_personal")
CON_DATA_PATH = REPO_ROOT / "data" / "Con Data.xlsx"
WAVEFORM_DIR = REPO_ROOT / "data" / "raw" / "Control_Ensemble_AnkBrach_CF" / "dot0"


def load_waveforms(subject_ids):
    """Load waveforms for list of subjects."""
    waveforms = {"carotid": [], "femoral": []}

    print(f"Loading waveforms for {len(subject_ids)} subjects...")
    for sub_id in subject_ids:
        mat_path = WAVEFORM_DIR / f"{sub_id}.mat"
        if not mat_path.exists():
            continue

        try:
            mat = scipy.io.loadmat(str(mat_path))
            # Structure: mat['carotid'] is (samples, beats) or (samples,)
            # We want ensemble average
            if "carotid" in mat:
                c_wav = np.mean(mat["carotid"], axis=1).flatten()
                waveforms["carotid"].append(c_wav)
            if "femoral" in mat:
                f_wav = np.mean(mat["femoral"], axis=1).flatten()
                waveforms["femoral"].append(f_wav)
        except Exception as e:
            print(f"Error loading {sub_id}: {e}")

    return waveforms


def plot_comparisons(deaths, survivors, outcome_name="CV Death"):
    """Plot mean waveforms with std shading."""
    plt.figure(figsize=(15, 6))

    # Carotid
    plt.subplot(1, 2, 1)

    # Process Survivors
    s_waves = load_waveforms(survivors)["carotid"]
    if s_waves:
        # Resample to common length (e.g. 250 samples)
        # For simplicity, assuming comparable length or truncation
        # Real implementation needs resampling
        min_len = min(len(w) for w in s_waves)
        s_mat = np.array([w[:min_len] for w in s_waves])
        s_mean = np.mean(s_mat, axis=0)
        s_std = np.std(s_mat, axis=0)

        x = np.arange(len(s_mean))
        plt.plot(x, s_mean, "b-", label=f"Survivors (n={len(s_waves)})")
        plt.fill_between(x, s_mean - s_std, s_mean + s_std, color="b", alpha=0.1)

    # Process Deaths
    d_waves = load_waveforms(deaths)["carotid"]
    if d_waves:
        min_len = min(len(w) for w in d_waves)
        d_mat = np.array([w[:min_len] for w in d_waves])
        d_mean = np.mean(d_mat, axis=0)
        d_std = np.std(d_mat, axis=0)

        x = np.arange(len(d_mean))
        plt.plot(
            x, d_mean, "r-", linewidth=2, label=f"{outcome_name} (n={len(d_waves)})"
        )
        plt.fill_between(x, d_mean - d_std, d_mean + d_std, color="r", alpha=0.1)

    plt.title("Carotid Waveform Comparison")
    plt.legend()
    plt.grid(True)

    # Save
    out_file = REPO_ROOT / "docs" / "plans" / "cv_death_comparison.png"
    plt.savefig(out_file)
    print(f"Plot saved to {out_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze CV Deaths")
    parser.add_argument(
        "--outcome_file", type=str, help="Path to file containing outcomes"
    )
    parser.add_argument(
        "--id_col", type=str, default="number", help="Subject ID column in outcome file"
    )
    parser.add_argument(
        "--target_col", type=str, default="CV_Death", help="Outcome column name"
    )
    args = parser.parse_args()

    # Load Con Data (Base)
    con_data = pd.read_excel(CON_DATA_PATH)

    # Load Outcome Data
    if args.outcome_file:
        print(f"Loading outcomes from {args.outcome_file}")
        if args.outcome_file.endswith(".csv"):
            outcomes = pd.read_csv(args.outcome_file)
        else:
            outcomes = pd.read_excel(args.outcome_file)

        # Merge
        merged = con_data.merge(
            outcomes, left_on="number", right_on=args.id_col, how="left"
        )
        target_col = args.target_col
    else:
        print(
            "No outcome file provided. Checking Con Data for 'NameOfCardiacDisease' == 'MI'"
        )
        merged = con_data
        # Create proxy target
        merged["is_MI"] = merged["NameOfCardiacDisease"].apply(
            lambda x: 1 if str(x) == "MI" else 0
        )
        target_col = "is_MI"

    # Analyze
    print(f"Target: {target_col}")
    print(merged[target_col].value_counts())

    deaths = merged[merged[target_col] == 1]["number"].tolist()
    survivors = merged[merged[target_col] == 0]["number"].tolist()

    print(f"Death IDs: {deaths}")

    # Plot
    plot_comparisons(deaths, survivors, outcome_name=target_col)


if __name__ == "__main__":
    main()
