"""Utility functions for Exploratory Data Analysis (02_eda.ipynb).

Keeps repetitive plotting configuration, multi-horizon return aggregation,
and automatic export of figures/tables to `results/` concise so that
`02_eda.ipynb` stays readable and focused on analysis and interpretation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr, shapiro, trim_mean

RESULTS_DIR = Path("results")
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"

PALETTE = {
    "Stocks": "#1f4e79",
    "10Y Gov Bonds": "#2e8b57",
    "1M T-Bills": "#d97706",
    "Inflation": "#b91c1c",
    "Deflation": "#2563eb",
    "Accent": "#7c3aed",
    "Neutral": "#64748b",
}


def ensure_results_dirs() -> None:
    """Create `results/figures` and `results/tables` if they do not exist."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def apply_plot_style() -> None:
    """Configure a consistent, publication-grade Matplotlib/Seaborn theme."""
    ensure_results_dirs()
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#cbd5e1",
            "axes.titleweight": "bold",
            "axes.titlesize": 12,
            "axes.labelsize": 10.5,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
            "legend.fontsize": 9.5,
            "legend.frameon": True,
            "legend.facecolor": "white",
            "legend.edgecolor": "#e2e8f0",
            "grid.color": "#e2e8f0",
            "grid.linestyle": "--",
            "grid.alpha": 0.7,
        }
    )


def save_fig(fig: plt.Figure, name: str) -> Path:
    """Save a Matplotlib figure into `results/figures/<name>.png`."""
    ensure_results_dirs()
    stem = name[:-4] if name.endswith(".png") else name
    out_path = FIGURES_DIR / f"{stem}.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    return out_path


def _df_to_markdown(df: pd.DataFrame, float_fmt: str = "{:.4f}") -> str:
    """Render a DataFrame cleanly as a GitHub-flavored Markdown table without extra deps."""
    work = df.copy()
    if work.index.name or not isinstance(work.index, pd.RangeIndex):
        idx_name = work.index.name or "index"
        work = work.reset_index().rename(columns={"index": idx_name})

    headers = [str(c) for c in work.columns]
    rows: list[list[str]] = []
    for _, row in work.iterrows():
        formatted_row = []
        for val in row:
            if pd.isna(val):
                formatted_row.append("")
            elif isinstance(val, (float, np.floating)):
                formatted_row.append(float_fmt.format(float(val)))
            else:
                formatted_row.append(str(val))
        rows.append(formatted_row)

    widths = [
        max(len(headers[j]), *(len(r[j]) for r in rows)) if rows else len(headers[j])
        for j in range(len(headers))
    ]
    header_line = "| " + " | ".join(headers[j].ljust(widths[j]) for j in range(len(headers))) + " |"
    sep_line = "| " + " | ".join("-" * widths[j] for j in range(len(headers))) + " |"
    body_lines = [
        "| " + " | ".join(r[j].ljust(widths[j]) for j in range(len(headers))) + " |"
        for r in rows
    ]
    return "\n".join([header_line, sep_line, *body_lines]) + "\n"


def save_table(
    df: pd.DataFrame,
    name: str,
    title: str | None = None,
    float_fmt: str = "{:.4f}",
    index: bool = True,
) -> tuple[Path, Path]:
    """Save a DataFrame as both `.csv` and readable `.md` inside `results/tables/`."""
    ensure_results_dirs()
    stem = name[:-4] if name.endswith(".csv") else name
    csv_path = TABLES_DIR / f"{stem}.csv"
    md_path = TABLES_DIR / f"{stem}.md"

    df.to_csv(csv_path, index=index)
    table_df = df if index else df.reset_index(drop=True)
    md_body = _df_to_markdown(table_df, float_fmt=float_fmt)
    if title:
        md_body = f"# {title}\n\n" + md_body
    md_path.write_text(md_body, encoding="utf-8")
    return csv_path, md_path


def load_clean_data(path: str | Path = "data/shiller_clean.csv") -> pd.DataFrame:
    """Load `shiller_clean.csv` and attach macroeconomic/valuation regime labels for EDA."""
    df = pd.read_csv(path, parse_dates=["date"], index_col="date")

    # Macroeconomic monetary & interest-rate eras
    eras = pd.Series(index=df.index, dtype="object")
    eras.loc[:"1926-05-01"] = "1. Pre-1926 (Gold Standard / Early)"
    eras.loc["1926-06-01":"1981-09-01"] = "2. 1926–1981 (Rising Yields & Great Inflation)"
    eras.loc["1981-10-01":"2020-12-01"] = "3. 1981–2020 (Disinflation & Rate Bull Market)"
    eras.loc["2021-01-01":] = "4. 2021–2026 (Post-COVID Inflation Reset)"
    df["era"] = pd.Categorical(
        eras,
        categories=[
            "1. Pre-1926 (Gold Standard / Early)",
            "2. 1926–1981 (Rising Yields & Great Inflation)",
            "3. 1981–2020 (Disinflation & Rate Bull Market)",
            "4. 2021–2026 (Post-COVID Inflation Reset)",
        ],
        ordered=True,
    )

    # Rolling 1-year inflation regimes
    inf_reg = pd.Series(index=df.index, dtype="object")
    inf_reg.loc[df["inf_1y"] < 0.0] = "Deflation (< 0%)"
    inf_reg.loc[(df["inf_1y"] >= 0.0) & (df["inf_1y"] < 0.03)] = "Low Inflation (0–3%)"
    inf_reg.loc[(df["inf_1y"] >= 0.03) & (df["inf_1y"] < 0.06)] = "Moderate Inflation (3–6%)"
    inf_reg.loc[df["inf_1y"] >= 0.06] = "High Inflation (>= 6%)"
    df["inflation_regime"] = pd.Categorical(
        inf_reg,
        categories=[
            "Deflation (< 0%)",
            "Low Inflation (0–3%)",
            "Moderate Inflation (3–6%)",
            "High Inflation (>= 6%)",
        ],
        ordered=True,
    )

    # CAPE valuation quartiles / regimes (historical thresholds)
    cape_reg = pd.Series(index=df.index, dtype="object")
    cape_reg.loc[df["cape"] < 12.0] = "Cheap (CAPE < 12)"
    cape_reg.loc[(df["cape"] >= 12.0) & (df["cape"] < 18.0)] = "Fair (12 <= CAPE < 18)"
    cape_reg.loc[(df["cape"] >= 18.0) & (df["cape"] < 25.0)] = "Expensive (18 <= CAPE < 25)"
    cape_reg.loc[df["cape"] >= 25.0] = "Bubble / Very Expensive (CAPE >= 25)"
    df["cape_regime"] = pd.Categorical(
        cape_reg,
        categories=[
            "Cheap (CAPE < 12)",
            "Fair (12 <= CAPE < 18)",
            "Expensive (18 <= CAPE < 25)",
            "Bubble / Very Expensive (CAPE >= 25)",
        ],
        ordered=True,
    )

    # Point-in-time inverse valuation yields (key linear-model feature candidates)
    df["earnings_yield"] = 1.0 / df["pe"]
    df["cape_yield"] = 1.0 / df["cape"]
    return df


def univariate_summary_table(
    df: pd.DataFrame,
    cols: Iterable[str],
    trimmed_prop: float = 0.05,
) -> pd.DataFrame:
    """Compute comprehensive DEA-04 Univariate Non-Graphical summary statistics.

    Includes counts, location (mean, 5% trimmed mean, median), spread (std, var,
    IQR, min, quartiles, max, range), shape (skewness, excess kurtosis),
    empirical 1-std coverage (68.3% for normal), and Shapiro-Wilk p-value.
    """
    records = []
    for col in cols:
        s = df[col].dropna()
        mean_val = float(s.mean())
        std_val = float(s.std(ddof=1))
        q25, q50, q75 = (float(x) for x in s.quantile([0.25, 0.50, 0.75]))
        within_1sd = float(((s >= mean_val - std_val) & (s <= mean_val + std_val)).mean())
        _, sw_p = shapiro(s)
        records.append(
            {
                "variable": col,
                "count": int(s.count()),
                "missing": int(df[col].isna().sum()),
                "mean": mean_val,
                "trimmed_mean_5pct": float(trim_mean(s.to_numpy(), trimmed_prop)),
                "median": q50,
                "std": std_val,
                "iqr": q75 - q25,
                "min": float(s.min()),
                "q25": q25,
                "q75": q75,
                "max": float(s.max()),
                "range": float(s.max() - s.min()),
                "skewness": float(s.skew()),
                "excess_kurtosis": float(s.kurtosis()),
                "within_1std_share": within_1sd,
                "shapiro_p": float(sw_p),
            }
        )
    return pd.DataFrame(records).set_index("variable")


def forward_annualized_return(tr_series: pd.Series, years: int) -> pd.Series:
    """Compute forward annualized return `(TR_{t+12*years} / TR_t)**(1/years) - 1`."""
    h = years * 12
    return (tr_series.shift(-h) / tr_series) ** (1.0 / years) - 1.0


def forward_cumulative_return(tr_series: pd.Series, years: int) -> pd.Series:
    """Compute forward cumulative total return `TR_{t+12*years} / TR_t - 1`."""
    h = years * 12
    return tr_series.shift(-h) / tr_series - 1.0


def multi_horizon_asset_summary(
    df: pd.DataFrame,
    horizons: Iterable[int] = (1, 3, 5, 10, 15, 20),
    start_date: str | None = None,
    real: bool = True,
) -> pd.DataFrame:
    """Summarize win probability and return distribution across horizons and asset classes."""
    sub = df.loc[start_date:] if start_date else df
    asset_cols = (
        {
            "Stocks": "tr_index",
            "10Y Gov Bonds": "bond10y_tr_real",
            "1M T-Bills": "tbill1m_tr_real",
        }
        if real
        else {
            "Stocks": "tr_index_nom",
            "10Y Gov Bonds": "bond10y_tr_nom",
            "1M T-Bills": "tbill1m_tr_nom",
        }
    )

    rows = []
    for yrs in horizons:
        for asset_name, col in asset_cols.items():
            ann = forward_annualized_return(sub[col], yrs).dropna()
            cum = forward_cumulative_return(sub[col], yrs).dropna()
            if ann.empty:
                continue
            rows.append(
                {
                    "horizon_years": yrs,
                    "asset": asset_name,
                    "n_windows": int(len(ann)),
                    "prob_positive_pct": float((ann > 0).mean() * 100.0),
                    "mean_ann_pct": float(ann.mean() * 100.0),
                    "median_ann_pct": float(ann.median() * 100.0),
                    "std_ann_pct": float(ann.std(ddof=1) * 100.0),
                    "iqr_ann_pct": float((ann.quantile(0.75) - ann.quantile(0.25)) * 100.0),
                    "min_ann_pct": float(ann.min() * 100.0),
                    "max_ann_pct": float(ann.max() * 100.0),
                    "median_terminal_wealth_per_1usd": float(1.0 + cum.median()),
                    "mean_terminal_wealth_per_1usd": float(1.0 + cum.mean()),
                }
            )
    return pd.DataFrame(rows)


def valuation_horizon_scan(
    df: pd.DataFrame,
    horizons: Iterable[int] = range(1, 21),
    start_date: str | None = None,
) -> pd.DataFrame:
    """Evaluate P/E, Earnings Yield (1/PE), CAPE, and CAPE Yield (1/CAPE) across horizons."""
    sub = df.loc[start_date:] if start_date else df
    rows = []
    for yrs in horizons:
        fwd = forward_annualized_return(sub["tr_index"], yrs)
        pe_df = pd.DataFrame({"pe": sub["pe"], "ey": 1.0 / sub["pe"], "fwd": fwd}).dropna()
        cape_df = pd.DataFrame({"cape": sub["cape"], "cy": 1.0 / sub["cape"], "fwd": fwd}).dropna()

        r_pe = float(pe_df["pe"].corr(pe_df["fwd"]))
        rho_pe = float(spearmanr(pe_df["pe"], pe_df["fwd"]).statistic)
        r_ey = float(pe_df["ey"].corr(pe_df["fwd"]))

        r_cape = float(cape_df["cape"].corr(cape_df["fwd"]))
        rho_cape = float(spearmanr(cape_df["cape"], cape_df["fwd"]).statistic)
        r_cy = float(cape_df["cy"].corr(cape_df["fwd"]))

        rows.append(
            {
                "horizon_years": int(yrs),
                "n_pe": int(len(pe_df)),
                "pe_pearson_r": r_pe,
                "pe_r2": r_pe**2,
                "pe_spearman_rho": rho_pe,
                "pe_spearman_rho2": rho_pe**2,
                "earnings_yield_r2": r_ey**2,
                "n_cape": int(len(cape_df)),
                "cape_pearson_r": r_cape,
                "cape_r2": r_cape**2,
                "cape_spearman_rho": rho_cape,
                "cape_spearman_rho2": rho_cape**2,
                "cape_yield_r2": r_cy**2,
            }
        )
    return pd.DataFrame(rows)
