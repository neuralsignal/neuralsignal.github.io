"""
Generate Vega-Lite JSON specs for the agentic workflow blog post.

Run: python3 gen_charts.py
Outputs: learning_curves.json, time_allocation.json
"""
import json
from pathlib import Path

OUT = Path(__file__).parent

# Blog palette (from WRITING_STYLE_GUIDE.md)
FOREST = "#2D6A4F"
TERRA = "#E07A5F"
AMBER = "#E8A838"
STEEL = "#3D85C6"
GRAY = "#6B7280"
FONT = "DM Sans, sans-serif"


def _config():
    """Shared Vega-Lite config for blog theme."""
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


def learning_curves():
    """Illustrative payoff curve for system-level workflows."""
    phases = [
        (0, 0.42, 0.92),
        (1, 0.40, 0.76),
        (2, 0.38, 0.60),
        (3, 0.37, 0.48),
        (4, 0.36, 0.38),
        (5, 0.35, 0.31),
        (6, 0.34, 0.28),
    ]

    data = []
    for stage, manual_effort, agentic_effort in phases:
        data.append({"stage": stage, "effort": manual_effort, "type": "Manual"})
        data.append({"stage": stage, "effort": agentic_effort, "type": "Agentic system"})

    payoff_region = {
        "mark": {"type": "rect", "opacity": 0.08},
        "data": {
            "values": [
                {
                    "x0": 4.75,
                    "x1": 6.45,
                    "y0": 0,
                    "y1": 1.0,
                }
            ]
        },
        "encoding": {
            "x": {"field": "x0", "type": "quantitative"},
            "x2": {"field": "x1"},
            "y": {"field": "y0", "type": "quantitative"},
            "y2": {"field": "y1"},
            "color": {"value": AMBER},
        },
    }

    lines = {
        "data": {"values": data},
        "mark": {
            "type": "line",
            "strokeWidth": 2.5,
            "interpolate": "monotone",
        },
        "encoding": {
            "x": {
                "field": "stage",
                "type": "quantitative",
                "title": "Time / repeated use",
                "scale": {"domain": [0, 6.6]},
                "axis": {
                    "labels": False,
                    "ticks": True,
                    "domain": True,
                    "grid": False,
                    "values": [0, 1, 2, 3, 4, 5, 6],
                },
            },
            "y": {
                "field": "effort",
                "type": "quantitative",
                "title": "Cost / effort",
                "scale": {"domain": [0.25, 1.0]},
                "axis": {
                    "labels": False,
                    "ticks": True,
                    "domain": True,
                    "grid": True,
                    "values": [0.3, 0.5, 0.7, 0.9],
                },
            },
            "color": {
                "field": "type",
                "type": "nominal",
                "title": None,
                "scale": {
                    "domain": ["Manual", "Agentic system"],
                    "range": [TERRA, FOREST],
                },
                "legend": None,
            },
            "strokeDash": {
                "field": "type",
                "type": "nominal",
                "scale": {
                    "domain": ["Manual", "Agentic system"],
                    "range": [[0], [6, 3]],
                },
                "legend": None,
            },
        },
    }

    payoff_label = {
        "mark": {
            "type": "text",
            "align": "left",
            "dx": 6,
            "dy": -8,
            "fontSize": 11,
            "fontStyle": "italic",
        },
        "data": {
            "values": [
                {
                    "stage": 5.0,
                    "effort": 0.50,
                    "label": "possible payoff region",
                }
            ]
        },
        "encoding": {
            "x": {"field": "stage", "type": "quantitative"},
            "y": {"field": "effort", "type": "quantitative"},
            "text": {"field": "label", "type": "nominal"},
            "color": {"value": AMBER},
        },
    }

    crossover_rule = {
        "mark": {
            "type": "rule",
            "strokeDash": [4, 3],
            "strokeWidth": 1.2,
            "opacity": 0.7,
        },
        "data": {"values": [{"stage": 4.55}]},
        "encoding": {
            "x": {"field": "stage", "type": "quantitative"},
            "color": {"value": GRAY},
        },
    }

    crossover_label = {
        "mark": {
            "type": "text",
            "align": "left",
            "dx": 5,
            "dy": -10,
            "fontSize": 11,
            "fontStyle": "italic",
        },
        "data": {"values": [{"stage": 4.55, "effort": 0.44, "label": "crossover"}]},
        "encoding": {
            "x": {"field": "stage", "type": "quantitative"},
            "y": {"field": "effort", "type": "quantitative"},
            "text": {"field": "label", "type": "nominal"},
            "color": {"value": GRAY},
        },
    }

    line_labels = {
        "mark": {
            "type": "text",
            "align": "left",
            "dx": 6,
            "fontSize": 12,
        },
        "data": {
            "values": [
                {"stage": 6.08, "effort": 0.34, "label": "manual", "color": TERRA},
                {
                    "stage": 6.08,
                    "effort": 0.28,
                    "label": "agentic system",
                    "color": FOREST,
                },
            ]
        },
        "encoding": {
            "x": {"field": "stage", "type": "quantitative"},
            "y": {"field": "effort", "type": "quantitative"},
            "text": {"field": "label", "type": "nominal"},
            "color": {"field": "color", "type": "nominal", "scale": None},
        },
    }

    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": {
            "text": "The delayed payoff",
            "subtitle": (
                "System-level workflows often start "
                "above manual cost and may pay back only after repeated use"
            ),
            "subtitleFontSize": 11,
            "subtitleColor": GRAY,
        },
        "width": "container",
        "height": 230,
        "layer": [payoff_region, lines, crossover_rule, payoff_label, crossover_label, line_labels],
    }
    return spec


def time_allocation():
    """Horizontal stacked bar: a typical day, before and after."""
    data = [
        {"mode": "Manual", "category": "Doing", "pct": 75},
        {"mode": "Manual", "category": "Review & Verify", "pct": 15},
        {"mode": "Manual", "category": "Coordination", "pct": 10},
        {"mode": "Manual", "category": "Context & Tools", "pct": 0},
        {"mode": "Manual", "category": "Knowledge Curation", "pct": 0},
        {"mode": "Manual", "category": "Agent Management", "pct": 0},
        {"mode": "Agentic", "category": "Doing", "pct": 10},
        {"mode": "Agentic", "category": "Review & Verify", "pct": 25},
        {"mode": "Agentic", "category": "Coordination", "pct": 10},
        {"mode": "Agentic", "category": "Context & Tools", "pct": 25},
        {"mode": "Agentic", "category": "Knowledge Curation", "pct": 20},
        {"mode": "Agentic", "category": "Agent Management", "pct": 10},
    ]
    data = [d for d in data if d["pct"] > 0]

    category_order = [
        "Doing",
        "Review & Verify",
        "Coordination",
        "Context & Tools",
        "Knowledge Curation",
        "Agent Management",
    ]

    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "config": _config(),
        "title": {
            "text": "A typical day, before and after",
            "subtitle": "Rough estimates, not measured data",
            "subtitleFontSize": 11,
            "subtitleColor": GRAY,
        },
        "width": "container",
        "height": 120,
        "data": {"values": data},
        "mark": {"type": "bar", "cornerRadiusEnd": 2},
        "encoding": {
            "y": {
                "field": "mode",
                "type": "nominal",
                "title": None,
                "axis": {"labelFontSize": 13, "labelFontWeight": "bold"},
                "sort": ["Manual", "Agentic"],
            },
            "x": {
                "field": "pct",
                "type": "quantitative",
                "title": "~% of time",
                "stack": "zero",
                "axis": {"format": "d"},
                "scale": {"domain": [0, 100]},
            },
            "color": {
                "field": "category",
                "type": "nominal",
                "title": None,
                "scale": {
                    "domain": category_order,
                    "range": [TERRA, AMBER, "#B0B0B0", FOREST, "#81B29A", STEEL],
                },
                "sort": category_order,
            },
            "order": {
                "field": "category",
                "type": "nominal",
                "sort": category_order,
            },
            "tooltip": [
                {"field": "mode", "type": "nominal"},
                {"field": "category", "type": "nominal"},
                {"field": "pct", "type": "quantitative", "title": "~%"},
            ],
        },
    }
    return spec


def main():
    specs = [
        ("learning_curves.json", learning_curves()),
        ("time_allocation.json", time_allocation()),
    ]
    for name, spec in specs:
        path = OUT / name
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        print(f"  wrote {path.name}")
    print(f"Done: {len(specs)} chart specs written.")


if __name__ == "__main__":
    main()
