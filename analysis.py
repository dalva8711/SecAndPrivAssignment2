# Analysis script for HR dataset chi-square and t-tests
# Usage: Run in an environment with pandas, numpy, scipy installed.
# This script expects 'HRDataset_v14.csv.xls' in the same directory or adjust the path.

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind

def main():
    path = "HRDataset_v14.csv.xls"
    try:
        df = pd.read_excel(path)
    except Exception:
        df = pd.read_csv(path)

    df.columns = [c.strip() for c in df.columns]

    def find_col(cands, cols):
        lc = [c.lower() for c in cols]
        for cand in cands:
            for i, name in enumerate(lc):
                if cand.lower() in name:
                    return cols[i]
        return None

    race_col = find_col(["RaceDesc", "Race", "Ethnicity"], df.columns)
    sex_col = find_col(["Sex", "Gender"], df.columns)
    termd_col = find_col(["Termd", "Terminated", "Termination", "Term"], df.columns)
    status_col = find_col(["EmploymentStatus", "Status"], df.columns)
    pay_col = find_col(["PayRate", "Salary", "HourlyRate", "AnnualSalary"], df.columns)
    perf_col = find_col(["PerformanceScore", "Performance", "Perf"], df.columns)

    # derive termination flag
    if termd_col is not None and df[termd_col].notna().any():
        terminated = pd.to_numeric(df[termd_col], errors="coerce").fillna(0)
        df["TerminatedFlag"] = (terminated != 0).astype(int)
    elif status_col is not None:
        df["TerminatedFlag"] = df[status_col].astype(str).str.contains("Terminated", case=False, na=False).astype(int)
    else:
        df["TerminatedFlag"] = np.nan

    # clean pay
    if pay_col is not None:
        df[pay_col] = df[pay_col].astype(str).str.replace(r"[\$,]", "", regex=True)
        df[pay_col] = pd.to_numeric(df[pay_col], errors="coerce")

    # perf ordinal
    if perf_col is not None:
        perf_order = ["PIP", "Needs Improvement", "Fully Meets", "Exceeds"]
        lower_map = {s.lower(): i for i, s in enumerate(perf_order)}
        df["PerformanceOrdinal"] = df[perf_col].astype(str).str.strip().str.lower().map(lower_map)

    # Claim 1
    out = []
    out.append("=== CLAIM 1 ===")
    if race_col and df["TerminatedFlag"].notna().any():
        sub = df[[race_col, "TerminatedFlag"]].dropna()
        tab = pd.crosstab(sub[race_col], sub["TerminatedFlag"])
        for need in [0,1]:
            if need not in tab.columns:
                tab[need] = 0
        tab = tab[[0,1]]
        chi2, p, dof, expected = chi2_contingency(tab.values)
        out.append(f"chi2={chi2:.4f}, dof={dof}, p={p:.6g}")
        rates = (tab[1] / tab.sum(axis=1)).sort_values(ascending=False)
        out.append("Termination rates by race:")
        for k,v in rates.items():
            out.append(f" - {k}: {v:.3%}")
    else:
        out.append("Insufficient data.")

    # Claim 2
    out.append("\n=== CLAIM 2 ===")
    if sex_col and pay_col and df[pay_col].notna().any():
        sub = df[[sex_col, pay_col]].dropna()
        males = sub[sub[sex_col].astype(str).str.lower().str.startswith("m")][pay_col]
        females = sub[sub[sex_col].astype(str).str.lower().str.startswith("f")][pay_col]
        if len(males) > 1 and len(females) > 1:
            t_stat, p_val = ttest_ind(males, females, equal_var=False, nan_policy='omit')
            out.append(f"male_n={len(males)}, female_n={len(females)}")
            out.append(f"male_mean={float(np.nanmean(males)):.2f}, female_mean={float(np.nanmean(females)):.2f}")
            out.append(f"t={t_stat:.4f}, p={p_val:.6g}")
        else:
            out.append("Not enough data.")
    else:
        out.append("Insufficient data.")

    # Claim 3
    out.append("\n=== CLAIM 3 ===")
    if race_col and perf_col and df[perf_col].notna().any():
        sub = df[[race_col, perf_col]].dropna()
        tab = pd.crosstab(sub[race_col], sub[perf_col])
        if tab.size > 0 and tab.shape[0] > 1 and tab.shape[1] > 1:
            chi2_3, p_3, dof_3, exp_3 = chi2_contingency(tab.values)
            out.append(f"Chi-square Race x Performance: chi2={chi2_3:.4f}, dof={dof_3}, p={p_3:.6g}")
        if df['PerformanceOrdinal'].notna().any():
            subo = df[[race_col, 'PerformanceOrdinal']].dropna()
            
            # Average performance scores by race
            out.append("\nAverage Performance Scores by Race (0=PIP, 1=Needs Improvement, 2=Fully Meets, 3=Exceeds):")
            perf_by_race = subo.groupby(race_col)['PerformanceOrdinal'].mean().sort_values(ascending=False)
            for race, avg_score in perf_by_race.items():
                out.append(f" - {race}: {avg_score:.3f}")
            
            is_min = ~subo[race_col].astype(str).str.contains("White", case=False, na=False)
            gmin = subo.loc[is_min, 'PerformanceOrdinal']
            gnon = subo.loc[~is_min, 'PerformanceOrdinal']
            if len(gmin) > 1 and len(gnon) > 1:
                out.append(f"\nMinority average: {float(np.mean(gmin)):.3f}")
                out.append(f"Non-minority average: {float(np.mean(gnon)):.3f}")
                t_stat3, p_val3 = ttest_ind(gmin, gnon, equal_var=False, nan_policy='omit')
                out.append(f"Ordinal t-test (Minority vs Non): t={t_stat3:.4f}, p={p_val3:.6g}")
    else:
        out.append("Insufficient data.")

    with open("results.txt", "w") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()