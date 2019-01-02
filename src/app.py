from flask import Flask, render_template
from src.common.database import Database





app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "rolandGarros"


@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():

    return render_template("home.html")

from models.users.views import user_blueprint
from models.alert.views import alert_blueprint
from models.stores.views import store_blueprint



app.register_blueprint(user_blueprint,url_prefix="/users")
app.register_blueprint(alert_blueprint,url_prefix="/alerts")
app.register_blueprint(store_blueprint,url_prefix="/stores")


