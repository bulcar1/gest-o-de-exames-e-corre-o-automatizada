from flask import Blueprint, render_template

home_route = Blueprint('home', __name__)

@home_route.route('/')
def home():
    return render_template('index.html')

@home_route.route('/exames')
def exames():
    return render_template('exames.html')

@home_route.route('/login')
def login():
    return render_template('login.html')