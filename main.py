from flask import Flask
from routes.home import home_bp
from routes.effect import effect_bp

app = Flask(__name__)
app.secret_key = "pixelcraft-secret-key"

app.register_blueprint(home_bp)
app.register_blueprint(effect_bp)

if __name__ == '__main__':
    app.run()
