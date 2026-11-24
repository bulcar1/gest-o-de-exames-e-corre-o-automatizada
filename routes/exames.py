from flask import Blueprint, render_template

home_route = Blueprint('exames', __name__)

@home_route.route('/')
def home():
    return render_template('exames.html')