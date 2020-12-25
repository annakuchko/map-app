from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import GeoJSONDataSource, ColorBar
from bokeh.models import DatetimeTickFormatter, PrintfTickFormatter, NumeralTickFormatter, NumeralTickFormatter
from bokeh.models import HoverTool, WheelZoomTool
from bokeh.models import LogColorMapper, LinearColorMapper
from bokeh.models import BasicTicker
from bokeh.models import Label
from app import config as cfg
from app import constants as cts
from app import data




def plot_map(ds, palette=cts.MAP_PALLETE, breeze=cfg.MAP_BREEZE):
    """Plot cases map."""

    # Calculating map bounds
    minx, miny, maxx, maxy = ds.total_bounds
    x_range = maxx - minx
    y_range = maxy - miny
    ar = (maxx - minx) / (maxy - miny)
    x_range = (minx - breeze * x_range, maxx + breeze * x_range)
    y_range = (miny - breeze * y_range, maxy + breeze * y_range)

    # Preparing data
    ds = GeoJSONDataSource(geojson=ds.to_json())
    tools = "pan,reset,save"
    color_mapper = LogColorMapper(palette=tuple(reversed(palette)))
    
    color_bar = ColorBar(color_mapper=color_mapper, major_label_text_font_size="7px",
                     ticker=BasicTicker(desired_num_ticks=len(tuple(reversed(palette)))),
                     label_standoff=6, border_line_color=None, location=(0, 0))
    

    p = figure(tools=tools, x_range=x_range, y_range=y_range, aspect_ratio=ar,
               x_axis_location=None, y_axis_location=None, match_aspect=True)

    p.grid.grid_line_color = None
    p.toolbar.logo = None
    p.add_layout(color_bar, 'right')

    p.patches('xs', 'ys', fill_alpha=0.7,
              fill_color={'field': 'total_color', 'transform': color_mapper},
              line_color='gray', line_width=0.25, source=ds)

    p.legend.location = "top_left"
    p.legend.click_policy="mute"
    #p.add_tools(HoverTool(tooltips=cts.MAP_TOOLTIP,
    #                      point_policy="follow_mouse",
    #                      toggleable=False))
    # Adding zoom tool
    wheel_zoom = WheelZoomTool(zoom_on_axis=False)
    p.add_tools(wheel_zoom)
    p.toolbar.active_scroll = wheel_zoom

    # Applying theme
    doc = curdoc()
    doc.theme = cfg.THEME
    return p
