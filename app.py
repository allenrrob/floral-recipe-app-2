from flask import Flask
from flask_scss import Scss

from extensions import db
from routes import (
    design_fees_bp,
    ingredient_types_bp,
    ingredients_bp,
    pages_bp,
    products_bp,
    quick_calculator_bp,
    vendors_bp,
)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Scss(app, static_dir="static", asset_dir="static/scss")

for blueprint in (
    pages_bp,
    ingredients_bp,
    products_bp,
    quick_calculator_bp,
    vendors_bp,
    ingredient_types_bp,
    design_fees_bp,
):
    app.register_blueprint(blueprint)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
