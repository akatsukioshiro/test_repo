from flask import Flask
from jynx_ui.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from jynx_ui import routes

