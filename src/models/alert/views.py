from flask import Blueprint, render_template,request,redirect,session,url_for
from models.alert.alert import Alert
from models.items.item import Item
import models.users.decorators as user_decorators



alert_blueprint = Blueprint('alerts',__name__)


@alert_blueprint.route('/')
def index():
    return "This is the alerts index"

@alert_blueprint.route('/new',methods=['GET','POST'])
@user_decorators.requires_login #redirct the user to 'users.login' if session['email'] is NOne
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name,url)
        item.save_to_mongo()

        alert = Alert(session['email'],price_limit,item._id)
        alert.load_item_price() #This already saves to MongoDB

        return redirect(url_for("users.user_alerts"))

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>',methods=['GET','POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        
        alert = Alert.find_by_id(alert_id)

        alert.price_limit = price_limit
        alert.save_to_mongo

        return redirect(url_for("users.user_alerts"))

    alert = Alert.find_by_id(alert_id)

    return render_template('alerts/edit_alert.html',alert=alert)

@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for("users.user_alerts"))

@alert_blueprint.route('/<string:alert_id>') # /alerts/<alert_id>
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/alert.html",alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page',alert_id=alert_id))

