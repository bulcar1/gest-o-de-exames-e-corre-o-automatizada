from flask import Flask
from database import criar_tabelas
from routes.home import home_route
from routes.login import login_route


app = Flask(__name__)


app.register_blueprint(home_route)
app.register_blueprint(login_route)


if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)