from flask import Flask
from routes.home import home_route
from database import criar_tabelas

app = Flask(__name__)

app.register_blueprint(home_route)

if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)