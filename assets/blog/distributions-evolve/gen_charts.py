"""
Generate Vega-Lite JSON specs for "letting a machine invent a distribution"
(Part 2 of the distributions series).

Run from this directory with the notebook_ideas environment, e.g.:
    cd ../../../../notebook_ideas && uv run python \
        ../neuralsignal.github.io/assets/blog/distributions-evolve/gen_charts.py

Outputs: trajectory.json, score_anomaly.json
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PERSONAL_ROOT = HERE.parents[3]
LOG_PATH = (
    PERSONAL_ROOT / "notebook_ideas" / "distribution_evolve"
    / "openevolve_output" / "logs" / "openevolve_20260108_142133.log"
)

# Blog palette (from WRITING_STYLE_GUIDE.md)
FOREST = "#2D6A4F"
TERRA = "#E07A5F"
STEEL = "#3D85C6"
AMBER = "#E8A838"
GRAY = "#6B7280"
HIST = "#9CA3AF"
FONT = "DM Sans, sans-serif"

# The standard to beat, from Part 1 (Johnson SU, per-day CV log-likelihood).
JOHNSON_SU = 3.275


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


_METRIC_RE = re.compile(r"cv_mean_ll=(-?[0-9.]+).*?valid=([0-9.]+)")


def parse_trajectory():
    """Walk the run log in order; keep each valid evaluation's CV log-likelihood.

    Returns a list of {eval, cv_ll, best} where best is the running maximum.
    """
    points = []
    best = None
    n = 0
    for line in LOG_PATH.read_text().splitlines():
        m = _METRIC_RE.search(line)
        if not m:
            continue
        cv_ll = float(m.group(1))
        valid = float(m.group(2))
        # Invalid candidates are scored with a huge sentinel; skip them.
        if valid < 1.0 or cv_ll < 0 or cv_ll > 6:
            continue
        n += 1
        if best is None or cv_ll > best:
            best = cv_ll
        points.append({"eval": n, "cv_ll": round(cv_ll, 4), "best": round(best, 4)})
    return points


def trajectory():
    points = parse_trajectory()
    last = points[-1]

    attempts = {
        "data": {"values": points},
        "mark": {"type": "circle", "size": 18, "opacity": 0.28, "color": HIST},
        "encoding": {
            "x": {"field": "eval", "type": "quantitative",
                  "title": "Candidate (in order of evaluation)"},
            "y": {"field": "cv_ll", "type": "quantitative",
                  "title": "CV log-likelihood per day",
                  "scale": {"domain": [2.9, 3.4]}},
            "tooltip": [
                {"field": "eval", "type": "quantitative", "title": "candidate"},
                {"field": "cv_ll", "type": "quantitative", "title": "CV log-lik / day"},
            ],
        },
    }

    best_line = {
        "data": {"values": points},
        "mark": {"type": "line", "color": FOREST, "strokeWidth": 2.5, "interpolate": "step-after"},
        "encoding": {
            "x": {"field": "eval", "type": "quantitative"},
            "y": {"field": "best", "type": "quantitative", "scale": {"domain": [2.9, 3.4]}},
        },
    }

    target_rule = {
        "data": {"values": [{"y": JOHNSON_SU}]},
        "mark": {"type": "rule", "color": TERRA, "strokeDash": [4, 3], "strokeWidth": 1.4},
        "encoding": {"y": {"field": "y", "type": "quantitative"}},
    }

    target_label = {
        "data": {"values": [{"eval": last["eval"], "y": JOHNSON_SU,
                             "label": "Johnson SU (best hand-designed)"}]},
        "mark": {"type": "text", "align": "right", "dy": -7, "fontSize": 11,
                 "fontStyle": "italic", "color": TERRA},
        "encoding": {
            "x": {"field": "eval", "type": "quantitative"},
            "y": {"field": "y", "type": "quantitative"},
            "text": {"field": "label", "type": "nominal"},
        },
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "Evolutionary search over candidate distributions",
        "width": "container",
        "height": 300,
        "layer": [attempts, best_line, target_rule, target_label],
    }


def score_anomaly():
    """CV log-likelihood of evolved candidates, one with a normalization bug.

    A properly normalized PDF cannot push per-day log-likelihood much above
    ~3.4 for this data. The buggy candidate reported 9.29 because its
    normalization constant did not match the kernel it actually evaluated.
    """
    rows = [
        {"run": "not normalized", "cv_ll": 9.29, "kind": "bug"},
        {"run": "3 params", "cv_ll": 3.318, "kind": "normalized"},
        {"run": "5 params", "cv_ll": 3.327, "kind": "normalized"},
        {"run": "9 params", "cv_ll": 3.350, "kind": "normalized"},
    ]
    order = ["not normalized", "3 params", "5 params", "9 params"]

    bars = {
        "mark": {"type": "bar", "cornerRadiusEnd": 2, "width": 42},
        "encoding": {
            "x": {"field": "run", "type": "nominal", "title": None, "sort": order,
                  "axis": {"labelFontSize": 13, "labelAngle": 0}},
            "y": {"field": "cv_ll", "type": "quantitative",
                  "title": "CV log-likelihood per day", "scale": {"domain": [0, 10]}},
            "color": {
                "field": "kind", "type": "nominal", "legend": None,
                "scale": {"domain": ["bug", "normalized"],
                          "range": [TERRA, FOREST]},
            },
            "tooltip": [
                {"field": "run", "type": "nominal", "title": "candidate"},
                {"field": "cv_ll", "type": "quantitative", "title": "CV log-lik / day"},
            ],
        },
    }

    ceiling = {
        "data": {"values": [{"y": 3.5}]},
        "mark": {"type": "rule", "color": GRAY, "strokeDash": [4, 3], "strokeWidth": 1.2},
        "encoding": {"y": {"field": "y", "type": "quantitative"}},
    }

    ceiling_label = {
        "data": {"values": [{"run": "5 params", "y": 3.5,
                             "label": "maximum for a normalized density"}]},
        "mark": {"type": "text", "align": "center", "dy": -7, "fontSize": 11,
                 "fontStyle": "italic", "color": GRAY},
        "encoding": {
            "x": {"field": "run", "type": "nominal", "sort": order},
            "y": {"field": "y", "type": "quantitative"},
            "text": {"field": "label", "type": "nominal"},
        },
    }

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": "Cross-validated log-likelihood of four evolved candidates",
        "width": "container",
        "height": 260,
        "data": {"values": rows},
        "layer": [bars, ceiling, ceiling_label],
    }


def main():
    pts = parse_trajectory()
    print(f"Parsed {len(pts)} valid candidates; best CV log-lik = {pts[-1]['best']}")
    specs = [
        ("trajectory.json", trajectory()),
        ("score_anomaly.json", score_anomaly()),
    ]
    for name, spec in specs:
        (HERE / name).write_text(json.dumps(spec, indent=2), encoding="utf-8")
        print(f"  wrote {name}")
    print(f"Done: {len(specs)} chart specs written.")


if __name__ == "__main__":
    main()
