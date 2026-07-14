#!/usr/bin/env python3
"""Render Supplementary Figure S2 for the v1.2 open reproducibility release.

Figure contract
---------------
Core conclusion: v1.2 provides a self-contained, independent evaluation route
because fixed partitions, labels, graph snapshot, checkpoints, score matrices,
and scoring code are public.
Archetype: schematic-led composite.
Panel A: public released assets; Panel B: external source boundaries; Panel C:
the independent evaluation route.  Counts are traceable to the source-data CSV.
"""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# Editable vector text and a restrained accessible palette.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 6.8

BLUE = "#0F4D92"
TEAL = "#2E7D72"
NEUTRAL = "#4D4D4D"
LIGHT = "#F4F7FA"
BORDER = "#9EB6D0"
PALE_BLUE = "#E8F0F8"
PALE_TEAL = "#E8F4F1"
PALE_GREY = "#F3F3F3"


def draw_panel(ax, label: str, title: str, rows: list[tuple[str, str]], footer: str, fill: str) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("auto")
    outer = FancyBboxPatch((0.01, 0.02), 0.98, 0.96, boxstyle="round,pad=0.008", linewidth=0.9,
                           edgecolor=BORDER, facecolor="white", transform=ax.transAxes)
    ax.add_patch(outer)
    ax.text(0.05, 0.93, label, transform=ax.transAxes, fontsize=10, fontweight="bold", color="#1E2A36")
    ax.text(0.13, 0.937, title, transform=ax.transAxes, fontsize=7.0, fontweight="bold", color="#1E2A36")
    n = len(rows)
    top, bottom, left, split, right = 0.82, 0.22, 0.06, 0.48, 0.94
    row_h = (top - bottom) / (n + 1)
    ax.add_patch(plt.Rectangle((left, top - row_h), right - left, row_h, transform=ax.transAxes,
                               facecolor=fill, edgecolor=BORDER, linewidth=0.5))
    ax.text(left + 0.025, top - row_h / 2, "Item", transform=ax.transAxes, va="center", fontsize=5.8, fontweight="bold")
    ax.text(split + 0.02, top - row_h / 2, "Status / access", transform=ax.transAxes, va="center", fontsize=5.8, fontweight="bold")
    for index, (item, status) in enumerate(rows):
        y = top - (index + 2) * row_h
        ax.add_patch(plt.Rectangle((left, y), right - left, row_h, transform=ax.transAxes,
                                   facecolor="white", edgecolor="#CDD8E5", linewidth=0.45))
        ax.plot([split, split], [y, y + row_h], transform=ax.transAxes, color="#CDD8E5", lw=0.45)
        ax.text(left + 0.025, y + row_h / 2, textwrap.fill(item, width=24), transform=ax.transAxes, va="center", color="#263442", fontsize=5.0)
        ax.text(split + 0.02, y + row_h / 2, textwrap.fill(status, width=27), transform=ax.transAxes, va="center", color=NEUTRAL, fontsize=5.0)
    footer_box = FancyBboxPatch((0.06, 0.08), 0.88, 0.095, boxstyle="round,pad=0.008", linewidth=0.5,
                                edgecolor="#C9D9EA", facecolor=PALE_BLUE if fill == PALE_BLUE else PALE_TEAL,
                                transform=ax.transAxes)
    ax.add_patch(footer_box)
    ax.text(0.5, 0.125, textwrap.fill(footer, width=54), transform=ax.transAxes, ha="center", va="center", color=BLUE, fontsize=5.3,
            wrap=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    figure_dir = root / "figures" / "supplementary"
    source_dir = root / "figures" / "source_data"
    figure_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    public_rows = [
        ("Fixed split and registries", "Public; 535 / 67 / 67 herbs"),
        ("Recorded-positive test labels", "Public; 8,632 pairs"),
        ("Candidate target universe", "Public; 2,309 targets"),
        ("Frozen graph snapshot", "Public; package-contained"),
        ("Best checkpoints", "Public; 25 frozen weights"),
        ("Score matrices and metrics", "Public; 25 matrices + scripts"),
    ]
    boundary_rows = [
        ("Dryad source tables", "Fetch from Dryad v6 (DOI recorded)"),
        ("ChEMBL source records", "Fetch from provider; attribution retained"),
        ("HGNC / UniProt / STRING records", "Fetch from original providers"),
        ("Provider credentials or private accounts", "Not included"),
        ("Historical sealed-access controls", "Not active in v1.2"),
    ]
    route_rows = [
        ("Verify package integrity", "Run checksum verifier"),
        ("Reproduce frozen scores", "Run public checkpoint scorer"),
        ("Evaluate any compatible model", "Submit NPZ with fixed axes"),
        ("Inspect raw logits / labels", "Load public matrices and label CSV"),
        ("Model selection", "Not permitted after public-test release"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.15))
    fig.subplots_adjust(left=0.015, right=0.985, bottom=0.02, top=0.98, wspace=0.08)
    draw_panel(
        axes[0], "A", "Public v1.2 reproducibility assets", public_rows,
        "All assets needed for fixed-test re-evaluation are included in this release.", PALE_BLUE,
    )
    draw_panel(
        axes[1], "B", "External source and licence boundaries", boundary_rows,
        "Raw provider records are linked and attributed rather than mirrored indiscriminately.", PALE_TEAL,
    )
    draw_panel(
        axes[2], "C", "Independent evaluation route", route_rows,
        "The fixed test set is public in v1.2; it is not a continuing sealed test.", PALE_GREY,
    )
    output_base = figure_dir / "supplementary_figure_S2"
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)

    rows = []
    for panel, values in [("A", public_rows), ("B", boundary_rows), ("C", route_rows)]:
        for item, status in values:
            rows.append({"panel": panel, "item": item, "status_or_access": status})
    rows.append({
        "panel": "global",
        "item": "Release boundary",
        "status_or_access": "Public fixed test; historical sealed evaluation occurred before disclosure; no post-release model selection.",
    })
    with (source_dir / "supplementary_figure_S2_source_data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["panel", "item", "status_or_access"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
