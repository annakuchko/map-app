"""Various data utilities."""
import pathlib
import pandas as pd
import geopandas as gpd
from app import config as cfg
def get_geo_data():
    """Read administrative borders."""
    root_dir = pathlib.Path(__file__).parent.parent
    geodata = gpd.read_file(root_dir.joinpath(cfg.GEODATA))
    return geodata
'''
def get_newest_data():
    """
    Calculate the most recent data for all regions.
    Return a dataframe indexed and sorted by date with column MultiIndex (region, category).
    To get a single region, do `df[region]` on return value.
    """

    root_dir = pathlib.Path(__file__).parent.parent
    #data = pd.read_csv(root_dir.joinpath(cfg.CSVDATA))
    data = pd.read_csv('https://raw.githubusercontent.com/annakuchko/map_app/main/data/sample_dat.csv?token=AP4TOMM5XO62EPAPWSMXKK27WDTFA')
    #data = pd.read_csv('https://raw.githubusercontent.com/annakuchko/datdat/main/sample_dat.csv', engine='python')
    data["date"] = pd.to_datetime(data["date"], dayfirst=True)
    data = data.set_index(["date", "category"]).unstack(level=-1)
    return data.sort_index()
'''
def get_region_data(df, region):
    """Get data. along with diffs for `region`."""
    # Get data for this region
    country_data = pd.DataFrame(df[region])
   
    country_data = (country_data
                    .join(country_data
                          .diff()
                          .rename(lambda cl: f"{cl}_diff", axis=1)))
    return country_data, country_data.iloc[-1].to_dict()
def get_rendered_page(page_name):
    """Get prerendered page, if available."""
    rendered = None
    root_dir = pathlib.Path(__file__).parent.parent
    filename = root_dir.joinpath(cfg.RENDERED_DIR).joinpath(f"{page_name}.html")
    if filename.exists():
        with open(filename, "r") as f:
            rendered = f.read()
    return rendered
def save_rendered_page(page_name, rendered):
    """Save prerendered page."""
    root_dir = pathlib.Path(__file__).parent.parent
    filename = root_dir.joinpath(cfg.RENDERED_DIR).joinpath(f"{page_name}.html")
    with open(filename, "w") as f:
        f.write(rendered)
def get_data_by_key(keys, ext=".csv", pandas=True, dt_cols=["date"], set_index=None, sort_by=None):
    """Read data from disk."""
    root_dir = pathlib.Path(__file__).parent.parent.joinpath(cfg.DATA_DIR)
    filename = root_dir.joinpath(*keys).with_suffix(ext)
    if filename.exists() and pandas:
        data = pd.read_csv(filename)
        for cl in dt_cols:
            data[cl] = pd.to_datetime(data[cl], dayfirst=True)
        if sort_by:
            data = data.sort_values(sort_by)
        if set_index is not None and set_index in data.columns:
            data.set_index(set_index, inplace=True)
        return data
    elif filename.exists():
        with open(filename, "r") as f:
            data = f.read()
        return data
    else:
        return None
def capitalize(s):
    """Capitalize only first letter."""
    return s[0].upper() + s[1:]
