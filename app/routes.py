"""Routes for mapper dashboard app."""
from flask import render_template
from app import map_app
from app import data
from app import plotting
from app import config as cfg
from app import constants as cts
from bokeh.embed import components
import io
import random
from flask import Flask, Response, request, redirect, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

def transform(text_file_contents):
    reader = csv.reader(text_file_contents)
    return reader

def filter_secondary_links(region, num_links=2):
    """Return `num_links` secondary links, except `region`."""
    return [link for link in cts.REGIONAL_LINKS if link["name"] != region][:num_links]

@map_app.route('/')
def form():
  return """
    <html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <title>
		 Картограмма регионов России
	</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css" />
    <link rel="stylesheet" href="/static/main.css">
  </head>
  <div class="container">
      <div class="container">
        <nav class="navbar navbar-expand-lg fixed-top navbar-fixed-width navbar-white ">
            <a href="/" class="navbar-brand"><h3>Картограмма регионов России</h3></a>
              </nav>
      </div>
      
        <body>
	    <div class="container">
	    <h2>Загрузите CSV файл</h2>
            <p class="footer-link mt-2"> Шаблон CSV <a href="https://github.com/annakuchko/datdat/raw/main/sample_data_for_mapper_app.xlsx" target="blank"> файла</a></p>
	    <p class="footer-link mt-2"> Поля date и category не изменять. Названия регионов должны полностью совпадать. После внесения данных файл нужно сохранить как "CSV UTF-8 (разделитель -- запятая) (*.CSV)"</p>
            
            <form action="/transform" method="post" enctype="multipart/form-data">
                <input type="file" name="data_file" />
                <input type="submit" />
            </form>
	    </div>
            
            <div class="container mt-5 pb-0 footer">
      <nav class="navbar">
        <div class="row" style="width: 100%;">
          
          
          <div class="col-lg-3">
              <h6 class="mt-2 mb-0 footer-link">About</h6>
              <p class="footer-link mt-2">С вопросами и предложениями писать на почту: <a href="mailto:anna.kuchko@yandex.ru" target="blank">anna.kuchko@yandex.ru</a></p>
	      <p class="footer-link mt-2">Другие опции будут добавляться по мере возможности.</p>
              <p class="footer-link mt-2">♡♡♡БАИС-2017♡♡♡</p>
	      <p class="footer-link mt-2"><a href="https://github.com/annakuchko/map_app" target="blank"> Source code</p>
              <p class="footer-link mt-2 blue-font" style="font-weight: 400;">Автор проекта: Анна Кучко, 2020.</p>
       
          </div>
        </div>
      </nav>
    </div>
    </div>
        </body>
    </html>
"""
@map_app.route('/transform', methods=["POST"])
def index():
    """Main page of the dashboard."""
    # Check pre-rendered HTML
    rendered = data.get_rendered_page("country")
    if rendered:
        return rendered
    city = "Россия"
    main_links = filter_secondary_links(city)
    secondary_links = []
    # Getting data
    #full_data = data.get_newest_data()

    #request_file = request.files['data_file']

    #df = pd.read_csv(request.files.get('data_file'))  
    df = pd.read_csv(request.files.get('data_file'), sep = ";")  
    #fstring = request_file.read()
    #csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]
    #df = pd.DataFrame.from_dict(csv_dicts)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df = df.set_index(["date", "category"]).unstack(level=-1)
    full_data = df.sort_index()
    del df
    
    country_data_full, country_data = data.get_region_data(full_data, city)
    # Map plot
    borders = data.get_geo_data()
    latest_data = full_data.iloc[-1].unstack(level=-1)
    latest_diff = (full_data
                   .diff()
                   .iloc[-1]
                   .unstack(level=-1)
                   .rename(lambda x: f"{x}_diff", axis=1))
    map_data = (borders
                .join(latest_data, on="REGION")
                .join(latest_diff, on="REGION")
                .fillna(0))
    
    map_data["total_color"] = 1. + map_data["total"]
    map_plot = plotting.plot_map(map_data)
 



    # Getting Bokeh components
    script, div = components({"map": map_plot})
    # Rendering HTML
    rendered = render_template("main.html", city=city,
                               main_links=main_links,
                               secondary_links=secondary_links,
                               bokeh_script=script,
                               **div)
    #data.save_rendered_page("country", rendered)
    del map_data

    return rendered
