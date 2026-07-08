"""Generate review-safe aggregate figure previews from public source-data files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "figures" / "source_data"
OUTPUT_DIR = REPO_ROOT / "aggregate_figure_previews"

EXPECTED_SOURCES = {
    "figure1_source_notes.csv": {"notes"},
    "figure2_source_notes.csv": {"notes"},
    "figure3_source_data.csv": {
        "panel",
        "model",
        "metric",
        "value_full_precision",
        "sd_full_precision",
        "value_display",
        "sd_display",
        "notes",
    },
    "supplementary_figure_S1_source_data.csv": {"panel", "ablation", "value"},
    "supplementary_figure_S2_source_notes.csv": {"notes"},
    "supplementary_figure_S3_source_data.csv": {"panel", "short_label", "value_full_precision"},
    "supplementary_figure_S4_source_data.csv": {"panel", "element", "metric"},
    "supplementary_figure_S5_source_data.csv": {"panel", "model", "metric", "value"},
}

SCHEMATIC_FIGURES = {
    "figure1": "figure1_source_notes.csv",
    "figure2": "figure2_source_notes.csv",
    "supplementary_figure_S2": "supplementary_figure_S2_source_notes.csv",
}


def source_path(name: str) -> Path:
    path = (SOURCE_DIR / name).resolve()
    if SOURCE_DIR.resolve() not in path.parents:
        raise ValueError(f"Refusing to read outside figures/source_data: {name}")
    return path


def load_source(name: str) -> pd.DataFrame:
    return pd.read_csv(source_path(name))


def check_sources() -> tuple[bool, list[str]]:
    issues = []
    for filename, required_columns in EXPECTED_SOURCES.items():
        path = source_path(filename)
        if not path.exists():
            issues.append(f"{filename}: missing")
            continue
        try:
            columns = set(pd.read_csv(path, nrows=0).columns)
        except Exception as exc:
            issues.append(f"{filename}: unreadable CSV: {exc}")
            continue
        missing_columns = sorted(required_columns - columns)
        if missing_columns:
            issues.append(f"{filename}: missing columns {', '.join(missing_columns)}")
    return not issues, issues


def save_current(name: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        plt.savefig(OUTPUT_DIR / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close()


def ordered_bar(ax, labels, values, errors=None, title="", ylabel=""):
    x = np.arange(len(labels))
    ax.bar(x, values, yerr=errors, capsize=4, color="#4C78A8", edgecolor="#333333", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.25)


def plot_figure3() -> None:
    df = load_source("figure3_source_data.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))

    panel_a = df[(df["panel"] == "A") & df["value_full_precision"].notna()].copy()
    ordered_bar(
        axes[0],
        panel_a["model"].tolist(),
        panel_a["value_full_precision"].astype(float).tolist(),
        panel_a["sd_full_precision"].replace("", np.nan).astype(float).tolist(),
        "A. Macro AUPR",
        "Mean",
    )

    panel_b = df[(df["panel"] == "B") & df["value_full_precision"].notna()].copy()
    ordered_bar(
        axes[1],
        panel_b["model"].tolist(),
        panel_b["value_full_precision"].astype(float).tolist(),
        None,
        "B. Difference vs reference",
        "Mean difference",
    )
    axes[1].axhline(0, color="#333333", linewidth=0.8)

    panel_c = df[(df["panel"] == "C") & df["value_full_precision"].notna()].copy()
    ordered_bar(
        axes[2],
        [f"{row.model} {row.metric}" for row in panel_c.itertuples()],
        panel_c["value_full_precision"].astype(float).tolist(),
        None,
        "C. Secondary metrics",
        "Mean",
    )
    fig.tight_layout()
    save_current("figure3_preview")


def plot_supplementary_figure_s1() -> None:
    df = load_source("supplementary_figure_S1_source_data.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    panel_a = df[(df["panel"] == "A") & df["seed"].notna()].copy()
    for idx, (_label, group) in enumerate(panel_a.groupby("ablation", sort=False)):
        axes[0].scatter([idx] * len(group), group["value"].astype(float), color="#4C78A8", s=22)
    axes[0].axhline(0, color="#333333", linewidth=0.8)
    axes[0].set_xticks(range(panel_a["ablation"].nunique()))
    axes[0].set_xticklabels(panel_a["ablation"].drop_duplicates().tolist(), rotation=35, ha="right")
    axes[0].set_title("A. Seed-level validation deltas")
    axes[0].set_ylabel("Delta macro AUPR")
    axes[0].grid(axis="y", alpha=0.25)

    panel_b = df[(df["panel"] == "B") & df["seed"].isna()].copy()
    ordered_bar(
        axes[1],
        panel_b["ablation"].tolist(),
        panel_b["value"].astype(float).tolist(),
        None,
        "B. Mean paired deltas",
        "Delta macro AUPR",
    )
    axes[1].axhline(0, color="#333333", linewidth=0.8)
    fig.tight_layout()
    save_current("supplementary_figure_S1_preview")


def plot_supplementary_figure_s3() -> None:
    df = load_source("supplementary_figure_S3_source_data.csv")
    panel = df[df["value_full_precision"].notna()].copy()
    panel = panel.sort_values("value_full_precision", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(panel["short_label"], panel["value_full_precision"].astype(float), color="#59A14F")
    ax.set_xlabel("Validation macro herb-level AUPR")
    ax.set_title("Validation-only baseline diagnostics")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    save_current("supplementary_figure_S3_preview")


def plot_supplementary_figure_s4() -> None:
    df = load_source("supplementary_figure_S4_source_data.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    panel_b = df[(df["panel"] == "B") & (df["metric"] == "validation_macro_herb_level_AUPR")].copy()
    ordered_bar(
        axes[0],
        panel_b["element"].tolist(),
        panel_b["value"].astype(float).tolist(),
        None,
        "B. NN stress variants",
        "Validation macro AUPR",
    )

    panel_c = df[(df["panel"] == "C") & (df["metric"] == "herb_count")].copy()
    ordered_bar(
        axes[1],
        panel_c["element"].tolist(),
        panel_c["value"].astype(float).tolist(),
        None,
        "C. Diagnostic counts",
        "Herb count",
    )
    fig.tight_layout()
    save_current("supplementary_figure_S4_preview")


def plot_supplementary_figure_s5() -> None:
    df = load_source("supplementary_figure_S5_source_data.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    seed_rows = df[df["seed"].astype(str).str.startswith("FINAL_", na=False)].copy()
    for idx, (_model, group) in enumerate(seed_rows.groupby("model", sort=False)):
        axes[0].scatter([idx] * len(group), group["value"].astype(float), color="#4C78A8", s=22)
    axes[0].set_xticks(range(seed_rows["model"].nunique()))
    axes[0].set_xticklabels(seed_rows["model"].drop_duplicates().tolist(), rotation=35, ha="right")
    axes[0].set_title("A. Final-seed macro AUPR")
    axes[0].set_ylabel("Macro AUPR")
    axes[0].grid(axis="y", alpha=0.25)

    mean_rows = df[df["metric"].astype(str).str.contains("mean_macro", na=False)].copy()
    if mean_rows.empty:
        mean_rows = df[df["mean"].notna()].drop_duplicates("model").copy()
    ordered_bar(
        axes[1],
        mean_rows["model"].tolist(),
        mean_rows["mean"].astype(float).tolist(),
        mean_rows.get("sd", pd.Series(dtype=float)).astype(float).tolist(),
        "B. Mean across final seeds",
        "Macro AUPR",
    )
    fig.tight_layout()
    save_current("supplementary_figure_S5_preview")


def write_schematic_notes() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Schematic Figure Source Notes", ""]
    for figure, source in SCHEMATIC_FIGURES.items():
        rows = load_source(source)
        lines.append(f"## {figure}")
        lines.append("")
        for _, row in rows.iterrows():
            compact = "; ".join(f"{col}: {row[col]}" for col in rows.columns if pd.notna(row[col]))
            lines.append(f"- {compact}")
        lines.append("")
    (OUTPUT_DIR / "schematic_source_notes.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-sources", action="store_true", help="Validate public source-data files only.")
    args = parser.parse_args()

    ok, issues = check_sources()
    if args.check_sources:
        if ok:
            print("PASS: source-data files present and schema-valid")
            return 0
        print("FAIL: source-data check failed")
        for issue in issues:
            print(issue)
        return 1

    if not ok:
        print("FAIL: source-data check failed")
        for issue in issues:
            print(issue)
        return 1

    plot_figure3()
    plot_supplementary_figure_s1()
    plot_supplementary_figure_s3()
    plot_supplementary_figure_s4()
    plot_supplementary_figure_s5()
    write_schematic_notes()
    print(f"PASS: generated aggregate figure previews in {OUTPUT_DIR.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
