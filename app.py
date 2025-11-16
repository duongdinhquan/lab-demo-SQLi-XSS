from flask import Flask
from config import Config
from views.routes import init_routes

app = Flask(__name__)
app.config.from_object(Config) # nạp các attribute của class config vào biến config của FLASK
app.config['SESSION_COOKIE_HTTPONLY'] = False

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)