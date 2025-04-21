from flask import Flask, jsonify, render_template, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
import pandas as pd
from routes.home import home_bp
from routes.auth import auth_bp
from routes.login import login_bp, db, login_manager
from routes.music import music_bp
from config import Config

app = Flask(__name__ )
app.template_folder='templates'
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login.login"
# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(music_bp, url_prefix='/music')

with app.app_context():
    db.create_all()



# Route for homepage with session check
@app.route("/")
def index():
    if "user_id" not in session:
        return "Unauthorized. Please login.", 403
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)