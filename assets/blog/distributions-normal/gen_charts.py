"""
Generate Vega-Lite JSON specs for the "problem with Normal" blog post.

Reads S&P 500 daily returns and fits standard distributions, then bakes the
computed values into self-contained Vega-Lite specs (no runtime data needed).

Run from this directory with the notebook_ideas environment, e.g.:
    cd ../../../../notebook_ideas && uv run python \
        ../neuralsignal.github.io/assets/blog/distributions-normal/gen_charts.py

Outputs: returns_hist.json, distribution_lineage.json, baseline_fit.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
# Sibling repos under .../personal/: neuralsignal.github.io and notebook_ideas
PERSONAL_ROOT = HERE.parents[3]
DATA_PATH = PERSONAL_ROOT / "notebook_ideas" / "distribution_evolve" / "data" / "values.parquet"
BASELINE_PATH = PERSONAL_ROOT / "notebook_ideas" / "distribution_evolve" / "baseline_results.json"

# Blog palette (from WRITING_STYLE_GUIDE.md)
FOREST = "#2D6A4F"
TERRA = "#E07A5F"
STEEL = "#3D85C6"
AMBER = "#E8A838"
PURPLE = "#5E4FA2"
GRAY = "#6B7280"
HIST = "#9CA3AF"
FONT = "DM Sans, sans-serif"


def _config():
    """Shared Vega-Lite config for the blog theme (works in light + dark)."""
    return {
        "background": "transparent",
        "font": FONT,
        "axis": {
            "labelFontSize": 12,
            "titleFontSize": 13,
            "titleFontWeight": "normal",
            "gridColor": "rgba(128,128,128,0.2)",
            "domainColor": GRAY,
            "tickColor": GRAY,
            "labelColor": GRAY,
            "titleColor": GRAY,
        },
        "legend": {
            "labelFontSize": 12,
            "titleFontSize": 13,
            "labelColor": GRAY,
            "titleColor": GRAY,
        },
        "title": {
            "fontSize": 15,
            "fontWeight": "normal",
            "color": GRAY,
        },
        "view": {"stroke": None},
    }


def load_returns():
    df = pd.read_parquet(DATA_PATH).dropna(subset=["value"])
    return df["value"].to_numpy()


def returns_hist(data):
    """Empirical return counts vs. the counts a Normal would predict (log y).

    The point: the Normal matches the body but is off by orders of magnitude
    in the tails, where the real crashes and rallies live.
    """
    mu, sigma = float(np.mean(data)), float(np.std(data))
    lo, hi = -0.16, 0.16
    binwidth = 0.004
    edges = np.arange(lo, hi + binwidth, binwidth)
    counts, _ = np.histogram(data, bins=edges)
    centers = (edges[:-1] + edges[1:]) / 2
    n = len(data)

    bars = []
    for c, k in zip(centers, counts):
        if k > 0:
            bars.append({"ret": round(float(c), 5), "count": int(k)})

    # Expected counts under the fitted Normal, on a fine grid.
    grid = np.linspace(lo, hi, 400)
    normal_counts = n * binwidth * stats.norm.pdf(grid, mu, sigma)
    line = [
        {"ret": round(float(x), 5), "count": float(max(y, 1e-6))}
        for x, y in zip(grid, normal_counts)
    ]

    y_scale = {"type": "log", "domain": [0.5, 4000], "clamp": True}

    bar_layer = {
        "data": {"values": bars},
        "mark": {"type": "bar", "color": HIST, "opacity": 0.85, "width": 2},
        "encoding": {
            "x": {"field": "ret", "type": "quantitative", "title": "Daily return",
                  "axis": {"format": "%"}, "scale": {"domain": [lo, hi]}},
            "y": {"field": "count", "type": "quantitative", "title": "Number of days",
                  "scale": y_scale},
            "tooltip": [
                {"field": "ret", "type": "quantitative", "title": "return", "format": ".1%"},
                {"field": "count", "type": "quantitative", "title": "days"},
            ],
        },
    }

    normal_layer = {
        "data": {"values": line},
        "mark": {"type": "line", "color": TERRA, "strokeWidth": 2.5},
        "encoding": {
            "x": {"field": "ret", "type": "quantitative", "scale": {"domain": [lo, hi]}},
            "y": {"field": "count", "type": "quantitative", "scale": y_scale},
        },
    }

    normal_label = {
        "data": {"values": [{"ret": 0.075, "count": 1.6, "label": "Normal fit"}]},
        "mark": {"type": "text", "align": "left", "fontSize": 12, "fontStyle": "italic"},
        "encoding": {
            "x": {"field": "ret", "type": "quantitative"},
            "y": {"field": "count", "type": "quantitative", "scale": y_scale},
            "text": {"field": "label", "type": "nominal"},
            "color": {"value": TERRA},
        },
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "97 years of S&P 500 daily returns",
        "width": "container",
        "height": 300,
        "layer": [bar_layer, normal_layer, normal_label],
    }


def distribution_lineage(data):
    """Empirical density with Normal, Student-t and Johnson SU overlaid (log y).

    Shows what each historical fix buys: the heavy-tailed and skewed families
    track the data into the tails where the Normal collapses.
    """
    lo, hi = -0.11, 0.11
    binwidth = 0.004
    edges = np.arange(lo, hi + binwidth, binwidth)
    counts, _ = np.histogram(data, bins=edges, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    bars = [
        {"ret": round(float(c), 5), "density": float(d)}
        for c, d in zip(centers, counts) if d > 0
    ]

    # Fit the three families the same way the baseline script does.
    norm_p = stats.norm.fit(data)
    t_p = stats.t.fit(data)
    jsu_p = stats.johnsonsu.fit(data)

    grid = np.linspace(lo, hi, 500)
    fits = {
        "Normal": stats.norm.pdf(grid, *norm_p),
        "Student-t": stats.t.pdf(grid, *t_p),
        "Johnson SU": stats.johnsonsu.pdf(grid, *jsu_p),
    }
    line_rows = []
    for name, pdf in fits.items():
        for x, y in zip(grid, pdf):
            line_rows.append({"ret": round(float(x), 5), "density": float(max(y, 1e-9)), "dist": name})

    y_scale = {"type": "log", "domain": [0.05, 120], "clamp": True}
    color_scale = {
        "domain": ["Normal", "Student-t", "Johnson SU"],
        "range": [TERRA, STEEL, FOREST],
    }

    bar_layer = {
        "data": {"values": bars},
        "mark": {"type": "bar", "color": HIST, "opacity": 0.6, "width": 2},
        "encoding": {
            "x": {"field": "ret", "type": "quantitative", "title": "Daily return",
                  "axis": {"format": "%"}, "scale": {"domain": [lo, hi]}},
            "y": {"field": "density", "type": "quantitative", "title": "Density",
                  "scale": y_scale},
        },
    }

    line_layer = {
        "data": {"values": line_rows},
        "mark": {"type": "line", "strokeWidth": 2.5},
        "encoding": {
            "x": {"field": "ret", "type": "quantitative", "scale": {"domain": [lo, hi]}},
            "y": {"field": "density", "type": "quantitative", "scale": y_scale},
            "color": {"field": "dist", "type": "nominal", "title": None, "scale": color_scale},
            "tooltip": [
                {"field": "dist", "type": "nominal", "title": "distribution"},
                {"field": "ret", "type": "quantitative", "title": "return", "format": ".1%"},
                {"field": "density", "type": "quantitative", "title": "density", "format": ".3f"},
            ],
        },
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "S&P 500 daily returns with three fitted distributions",
        "width": "container",
        "height": 320,
        "layer": [bar_layer, line_layer],
    }


def baseline_fit():
    """Per-observation cross-validated log-likelihood for the standard families.

    Two panels sharing a row order: the raw log-likelihood per day on the left,
    and the same numbers translated into "how much more probable is a typical
    day under this model than under the Normal" on the right. The second panel
    is just exp(ll - ll_normal) - 1, which is the per-day likelihood ratio and
    the most interpretable form of a log-likelihood gap.
    """
    results = json.loads(BASELINE_PATH.read_text())
    # Drop the evolved distribution; it belongs to Part 3.
    # Collapse the two near-identical t variants to keep the chart legible.
    keep = [r for r in results if r["name"] not in ("Evolved", "Non-central t")]
    best = max(r["cv_mean_ll"] for r in keep)
    normal_ll = next(r["cv_mean_ll"] for r in keep if r["name"] == "Normal")
    rows = [
        {"dist": r["name"], "cv_ll": round(r["cv_mean_ll"], 4),
         # Per-day likelihood ratio vs the Normal, as a fraction (0.24 = +24%).
         "ratio": round(float(np.exp(r["cv_mean_ll"] - normal_ll) - 1.0), 4),
         "is_best": r["cv_mean_ll"] == best}
        for r in keep
    ]

    y_enc = {"field": "dist", "type": "nominal", "title": None,
             "sort": {"field": "cv_ll", "order": "descending"},
             "axis": {"labelFontSize": 13}}
    color_enc = {
        "condition": {"test": "datum.is_best", "value": FOREST},
        "value": HIST,
    }

    baseline = 3.0
    ll_scale = {"domain": [baseline, 3.32], "nice": False}

    # Left panel: bars span from a non-zero baseline (3.0) to each value via
    # x/x2, so the small differences are visible without the zero-anchored bars
    # collapsing.
    ll_bars = {
        "mark": {"type": "bar", "cornerRadiusEnd": 2},
        "encoding": {
            "y": y_enc,
            "x": {"field": "cv_ll", "type": "quantitative",
                  "title": "Log-likelihood per day (higher is better)",
                  "scale": ll_scale},
            "x2": {"datum": baseline},
            "color": color_enc,
            "tooltip": [
                {"field": "dist", "type": "nominal", "title": "distribution"},
                {"field": "cv_ll", "type": "quantitative", "title": "CV log-lik / day"},
                {"field": "ratio", "type": "quantitative",
                 "title": "vs Normal / day", "format": "+.1%"},
            ],
        },
    }
    ll_labels = {
        "mark": {"type": "text", "align": "left", "dx": 4, "fontSize": 11, "color": GRAY},
        "encoding": {
            "y": y_enc,
            "x": {"field": "cv_ll", "type": "quantitative", "scale": ll_scale},
            "text": {"field": "cv_ll", "type": "quantitative", "format": ".3f"},
        },
    }

    max_ratio = max(r["ratio"] for r in rows)
    ratio_scale = {"domain": [0, max_ratio * 1.18], "nice": False}

    # Right panel: same rows, zero-anchored, showing the per-day likelihood
    # ratio relative to the Normal. The Normal sits at 0% by construction.
    ratio_bars = {
        "mark": {"type": "bar", "cornerRadiusEnd": 2},
        "encoding": {
            "y": {**y_enc, "axis": None},
            "x": {"field": "ratio", "type": "quantitative",
                  "title": "How much more likely per day than the Normal",
                  "axis": {"format": "+.0%"}, "scale": ratio_scale},
            "color": color_enc,
            "tooltip": [
                {"field": "dist", "type": "nominal", "title": "distribution"},
                {"field": "ratio", "type": "quantitative",
                 "title": "vs Normal / day", "format": "+.1%"},
            ],
        },
    }
    ratio_labels = {
        "mark": {"type": "text", "align": "left", "dx": 4, "fontSize": 11, "color": GRAY},
        "encoding": {
            "y": {**y_enc, "axis": None},
            "x": {"field": "ratio", "type": "quantitative", "scale": ratio_scale},
            "text": {"field": "ratio", "type": "quantitative", "format": "+.1%"},
        },
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "Cross-validated log-likelihood per day",
        "data": {"values": rows},
        "spacing": 44,
        "hconcat": [
            {
                "width": 300,
                "height": 220,
                "layer": [ll_bars, ll_labels],
            },
            {
                "width": 170,
                "height": 220,
                "layer": [ratio_bars, ratio_labels],
            },
        ],
    }


def main():
    data = load_returns()
    print(
        f"Loaded {len(data)} returns; skew={stats.skew(data):.4f}, "
        f"excess kurtosis={stats.kurtosis(data):.4f}"
    )
    specs = [
        ("returns_hist.json", returns_hist(data)),
        ("distribution_lineage.json", distribution_lineage(data)),
        ("baseline_fit.json", baseline_fit()),
    ]
    for name, spec in specs:
        path = HERE / name
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        print(f"  wrote {path.name}")
    print(f"Done: {len(specs)} chart specs written.")


if __name__ == "__main__":
    main()
