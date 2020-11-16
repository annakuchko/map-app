from flask import Flask

map_app = Flask(__name__,
            static_folder="../static",
            template_folder="../static/templates")
map_app.jinja_env.auto_reload = True
map_app.config['TEMPLATES_AUTO_RELOAD'] = True

from app import routes
