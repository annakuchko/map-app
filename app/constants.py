import pandas as pd
from bokeh.palettes import Reds, RdBu, Blues, GnBu
REGIONAL_LINKS = [{"name": "Россия", "link": "/"}]
# Categories
CATEGORIES = "total"
LEGEND_MAP = "1"
# Colors
COLOR_RAMP = ["#073763", "#990800"]
MAP_PALLETE = GnBu[9]
AGES_COLOR_RAMP = ["#38761d", "#417ab0", "#073763", "#e50b00", "#990800"]
DISCHARGES_COLOR_RAMP = ["#990800", "#38761d"]
# Tooltips
CASES_TOOLTIP = """<div class="plot-tooltip">
    <h4>{city}</h4>
    <div>
        <span style="font-weight: bold;">Дата: </span>@date_str
    </div>"""
CASES_TOOLTIP_FOOTER = """<div>
        <span style="font-weight: bold;">{value_type}: </span>@{col}{fmt}
    </div>
</div>
"""
MAP_TOOLTIP = """
<div class="plot-tooltip">
    <div class="mb-2">
        <h4>@REGION</h4>
    </div>
    <div>
        <span style="font-weight: bold;">Показатель: </span>@total{0,0}
    </div>
</div>
"""
