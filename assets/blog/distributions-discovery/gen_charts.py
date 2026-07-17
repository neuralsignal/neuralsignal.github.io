"""
Generate Vega-Lite JSON specs for "what the machine found" (Part 3).

Loads the evolved distribution, fits it on the S&P 500 returns, and bakes the
computed densities and comparison numbers into self-contained specs.

Run from this directory with the notebook_ideas environment, e.g.:
    cd ../../../../notebook_ideas && uv run python \
        ../neuralsignal.github.io/assets/blog/distributions-discovery/gen_charts.py

Outputs: evolved_overlay.json, baseline_with_evolved.json, params_vs_fit.json,
holdout_eval.json (requires distribution_evolve/holdout_results.json from
holdout_test.py)
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
PERSONAL_ROOT = HERE.parents[3]
EVOLVE_DIR = PERSONAL_ROOT / "notebook_ideas" / "distribution_evolve"
DATA_PATH = EVOLVE_DIR / "data" / "values.parquet"
BASELINE_PATH = EVOLVE_DIR / "baseline_results.json"
HOLDOUT_PATH = EVOLVE_DIR / "holdout_results.json"
# Labels use effective parameter counts (independently data-estimated quantities),
# not the programs' self-reported n_params() (3, 5, 9 respectively).
EVOLVED_PROGRAMS = {
    "Model 1 (4 params)": EVOLVE_DIR / "openevolve_output_v9_look" / "best" / "best_program.py",
    "Model 2 (4 params)": EVOLVE_DIR / "openevolve_output_v10_look" / "best" / "best_program.py",
    "Model 3 (5 params)": EVOLVE_DIR / "openevolve_output" / "best" / "best_program.py",
}
EVOLVED_N_PARAMS = {
    "Model 1 (4 params)": 4,
    "Model 2 (4 params)": 4,
    "Model 3 (5 params)": 5,
}

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
        "title": {"fontSize": 15, "fontWeight": "normal", "color": GRAY},
        "view": {"stroke": None},
    }


def load_returns():
    return pd.read_parquet(DATA_PATH).dropna(subset=["value"])["value"].to_numpy()


def load_holdout_results():
    """Results from holdout_test.py, keyed by distribution name.

    Contains `train_cv_ll_renorm` (training CV log-likelihood with each density
    divided by its numerically computed integral) and `holdout_mean_ll` (same,
    scored on the post-2025 returns).
    """
    payload = json.loads(HOLDOUT_PATH.read_text())
    return payload, {r["name"]: r for r in payload["results"]}


def load_evolved(path, tag):
    """Import an evolved Distribution class straight from its source file."""
    spec = importlib.util.spec_from_file_location(f"best_program_{tag}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Distribution


def evolved_overlay(data):
    lo, hi = -0.11, 0.11
    binwidth = 0.004
    edges = np.arange(lo, hi + binwidth, binwidth)
    counts, _ = np.histogram(data, bins=edges, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    bars = [
        {"ret": round(float(c), 5), "density": float(d)}
        for c, d in zip(centers, counts) if d > 0
    ]

    grid = np.linspace(lo, hi, 500)
    mu, std = np.mean(data), np.std(data)
    wide = np.linspace(mu - 30 * std, mu + 30 * std, 20001)

    norm_p = stats.norm.fit(data)
    jsu_p = stats.johnsonsu.fit(data)
    fits = {
        "Normal": stats.norm.pdf(grid, *norm_p),
        "Johnson SU": stats.johnsonsu.pdf(grid, *jsu_p),
    }
    for name, path in EVOLVED_PROGRAMS.items():
        Distribution = load_evolved(path, name)
        evo = Distribution()
        evo.fit(data)
        # Divide by the numerically computed integral so the curve is a true density.
        integral = np.trapezoid(np.exp(np.clip(evo.log_pdf(wide), -700, 700)), wide)
        fits[name] = np.exp(evo.log_pdf(grid)) / integral

    line_rows = []
    for name, pdf in fits.items():
        for x, y in zip(grid, pdf):
            line_rows.append({"ret": round(float(x), 5), "density": float(max(y, 1e-9)), "dist": name})

    # Floor low enough to show the tail region where the evolved variants differ
    # (single-count histogram bins sit at ~0.01).
    y_scale = {"type": "log", "domain": [0.005, 120], "clamp": True}
    color_scale = {
        "domain": ["Normal", "Johnson SU", *EVOLVED_PROGRAMS.keys()],
        "range": [TERRA, STEEL, FOREST, AMBER, PURPLE],
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
        "mark": {"type": "line", "strokeWidth": 2},
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
        "title": "S&P 500 daily returns with the evolved distributions fitted",
        "width": "container",
        "height": 320,
        "layer": [bar_layer, line_layer],
    }


def band_decomposition(data):
    """Mean log-likelihood per day by move size, relative to the Johnson SU.

    All models fit on the full history; evolved densities divided by their
    numerically computed integral. Shows where each evolved variant earns
    (and loses) its score.
    """
    mu, std = np.mean(data), np.std(data)
    wide = np.linspace(mu - 30 * std, mu + 30 * std, 20001)

    jsu_ll = stats.johnsonsu(*stats.johnsonsu.fit(data)).logpdf(data)
    model_lls = {}
    for name, path in EVOLVED_PROGRAMS.items():
        Distribution = load_evolved(path, f"bands_{name}")
        evo = Distribution()
        evo.fit(data)
        integral = np.trapezoid(np.exp(np.clip(evo.log_pdf(wide), -700, 700)), wide)
        model_lls[name] = evo.log_pdf(data) - np.log(integral)

    bands = [
        ("<0.5%", 0.0, 0.005),
        ("0.5-1%", 0.005, 0.01),
        ("1-3%", 0.01, 0.03),
        ("3-6%", 0.03, 0.06),
        (">6%", 0.06, np.inf),
    ]
    absr = np.abs(data)
    rows = []
    band_labels = []
    for label, a, b in bands:
        mask = (absr >= a) & (absr < b)
        full_label = f"{label} ({mask.sum():,} days)"
        band_labels.append(full_label)
        for name, ll in model_lls.items():
            diff = float(np.mean(ll[mask]) - np.mean(jsu_ll[mask]))
            rows.append({
                "band": full_label,
                "dist": name,
                "diff": round(diff, 4),
                "factor": round(float(np.exp(diff)), 4),
            })

    color_scale = {
        "domain": list(EVOLVED_PROGRAMS.keys()),
        "range": [FOREST, AMBER, PURPLE],
    }
    bars = {
        "mark": {"type": "bar", "cornerRadiusEnd": 2},
        "encoding": {
            "x": {"field": "band", "type": "nominal", "sort": band_labels,
                  "title": "Size of the daily move", "axis": {"labelAngle": 0}},
            "xOffset": {"field": "dist"},
            "y": {"field": "diff", "type": "quantitative",
                  "title": "Log-likelihood per day vs Johnson SU"},
            "color": {"field": "dist", "type": "nominal", "title": None,
                      "scale": color_scale},
            "tooltip": [
                {"field": "dist", "type": "nominal", "title": "distribution"},
                {"field": "band", "type": "nominal", "title": "move size"},
                {"field": "factor", "type": "quantitative",
                 "title": "times as probable as Johnson SU", "format": ".2f"},
            ],
        },
    }
    zero_rule = {
        "mark": {"type": "rule", "color": GRAY, "strokeWidth": 1},
        "encoding": {"y": {"datum": 0}},
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "Log-likelihood per day by move size, relative to the Johnson SU",
        "width": "container",
        "height": 300,
        "data": {"values": rows},
        "layer": [bars, zero_rule],
    }


def baseline_with_evolved():
    """Same two-panel layout as Part 1's baseline chart, evolved included.

    Left: per-day CV log-likelihood from a non-zero baseline. Right: the same
    numbers as per-day likelihood ratios vs the Normal (exp(ll - ll_normal) - 1).
    Values come from holdout_test.py's renormalized CV (each density divided
    by its integral), with all three evolved variants shown.
    """
    _, by_name = load_holdout_results()
    names = ["Normal", "Laplace", "Student t", "Skew Normal", "Johnson SU",
             *EVOLVED_PROGRAMS.keys()]
    lls = {n: by_name[n]["train_cv_ll_renorm"] for n in names}
    best = max(lls.values())
    normal_ll = lls["Normal"]
    rows = [
        {"dist": name, "cv_ll": round(ll, 4),
         "ratio": round(float(np.exp(ll - normal_ll) - 1.0), 4),
         "is_best": ll == best}
        for name, ll in lls.items()
    ]

    y_enc = {"field": "dist", "type": "nominal", "title": None,
             "sort": {"field": "cv_ll", "order": "descending"},
             "axis": {"labelFontSize": 13}}
    color_enc = {
        "condition": {"test": "datum.is_best", "value": FOREST},
        "value": HIST,
    }

    baseline = 3.0
    ll_scale = {"domain": [baseline, 3.40], "nice": False}

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
                "height": 240,
                "layer": [ll_bars, ll_labels],
            },
            {
                "width": 170,
                "height": 240,
                "layer": [ratio_bars, ratio_labels],
            },
        ],
    }


def params_vs_fit():
    """Parameter count vs. fit quality: standard families and the evolved variants."""
    baseline = json.loads(BASELINE_PATH.read_text())
    n_params = {r["name"]: r["n_params"] for r in baseline}
    _, by_name = load_holdout_results()
    points = []
    for name in ["Normal", "Laplace", "Skew Normal", "Student t", "Johnson SU"]:
        points.append({"label": name, "n_params": n_params[name],
                       "cv_ll": round(by_name[name]["train_cv_ll_renorm"], 4),
                       "kind": "hand-designed"})
    for name, k in EVOLVED_N_PARAMS.items():
        points.append({"label": name, "n_params": k,
                       "cv_ll": round(by_name[name]["train_cv_ll_renorm"], 4),
                       "kind": "evolved"})
    # Nudge label positions so the pile-up at 4 params stays readable
    label_shift = {"Johnson SU": -0.012}
    for p in points:
        p["label_y"] = round(p["cv_ll"] + label_shift.get(p["label"], 0.0), 4)

    base = {
        "mark": {"type": "point", "filled": True, "size": 110},
        "encoding": {
            "x": {"field": "n_params", "type": "quantitative",
                  "title": "Number of parameters", "scale": {"domain": [1.5, 6.5]},
                  "axis": {"values": [2, 3, 4, 5, 6]}},
            "y": {"field": "cv_ll", "type": "quantitative",
                  "title": "CV log-likelihood per day", "scale": {"domain": [3.0, 3.4]}},
            "color": {"field": "kind", "type": "nominal", "title": None,
                      "scale": {"domain": ["hand-designed", "evolved"],
                                "range": [HIST, FOREST]}},
            "tooltip": [
                {"field": "label", "type": "nominal", "title": "model"},
                {"field": "n_params", "type": "quantitative", "title": "params"},
                {"field": "cv_ll", "type": "quantitative", "title": "CV log-lik / day"},
            ],
        },
    }
    labels = {
        "mark": {"type": "text", "align": "left", "dx": 8, "dy": 0, "fontSize": 10.5, "color": GRAY},
        "encoding": {
            "x": {"field": "n_params", "type": "quantitative"},
            "y": {"field": "label_y", "type": "quantitative"},
            "text": {"field": "label", "type": "nominal"},
        },
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "Fit quality vs. number of parameters",
        "width": "container",
        "height": 300,
        "data": {"values": points},
        "layer": [base, labels],
    }


def holdout_eval():
    """Same two-panel layout as the baseline chart, scored on the unseen 2026 returns.

    Left: log-likelihood per day on the held-out period. Right: the same numbers
    as per-day likelihood ratios vs the Normal. Reads holdout_results.json
    (produced by distribution_evolve/holdout_test.py).
    """
    payload, by_name = load_holdout_results()
    names = ["Normal", "Laplace", "Student t", "Skew Normal", "Johnson SU",
             *EVOLVED_PROGRAMS.keys()]
    lls = {n: by_name[n]["holdout_mean_ll"] for n in names}
    best = max(lls.values())
    normal_ll = lls["Normal"]
    rows = [
        {"dist": name, "cv_ll": round(ll, 4),
         "ratio": round(float(np.exp(ll - normal_ll) - 1.0), 4),
         "is_best": ll == best}
        for name, ll in lls.items()
    ]

    y_enc = {"field": "dist", "type": "nominal", "title": None,
             "sort": {"field": "cv_ll", "order": "descending"},
             "axis": {"labelFontSize": 13}}
    color_enc = {
        "condition": {"test": "datum.is_best", "value": FOREST},
        "value": HIST,
    }

    baseline = 3.0
    ll_scale = {"domain": [baseline, 3.40], "nice": False}

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
                {"field": "cv_ll", "type": "quantitative", "title": "log-lik / day"},
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

    start, end = payload["holdout_start"], payload["holdout_end"]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": f"Log-likelihood per day on the held-out returns ({start} to {end})",
        "data": {"values": rows},
        "spacing": 44,
        "hconcat": [
            {
                "width": 300,
                "height": 240,
                "layer": [ll_bars, ll_labels],
            },
            {
                "width": 170,
                "height": 240,
                "layer": [ratio_bars, ratio_labels],
            },
        ],
    }


def main():
    data = load_returns()
    print(f"Loaded {len(data)} returns")
    specs = [
        ("evolved_overlay.json", evolved_overlay(data)),
        ("band_decomposition.json", band_decomposition(data)),
        ("baseline_with_evolved.json", baseline_with_evolved()),
        ("params_vs_fit.json", params_vs_fit()),
        ("holdout_eval.json", holdout_eval()),
    ]
    for name, spec in specs:
        (HERE / name).write_text(json.dumps(spec, indent=2), encoding="utf-8")
        print(f"  wrote {name}")
    print(f"Done: {len(specs)} chart specs written.")


if __name__ == "__main__":
    main()
