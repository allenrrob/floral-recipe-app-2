import os
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

# Floral Recipe App 
app = Flask(__name__)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
Scss(app, static_dir='static', asset_dir='static/scss')

# Import models so SQLAlchemy is aware of them
import models 

# App Routes
# --- Home page ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Ingredient Manager ---
@app.route('/ingredients')
def ingredients():
    return "Ingredient Manager (Step 5)"

# --- Product Manager ---
@app.route('/products')
def products():
    return "Products & Recipe Builder (Step 6)"

# --- Quick Calculaotr ---
@app.route('/temp-calculator')
def temp_calculator():
    return "Quick Design Calculator (Step 7)"

# --- Design Fee Manager ---
@app.route('/design-fees', METHODS=['GET', 'POST'])
def design_fees():
    if request.method == 'POST':
        name = requeset.form.get('name')
        fee_pct = request.form.get('design_fee_percentage')
        if name and fee_pct:
            new_fee = models.DesignType(name=name, design_fee_percentage=float(fee_pct))
            db.session.add(new_fee)
            db.session.commit()
            return redirect('/design-fees')

    all_fees = models.DesignType.query.all()
    return render_template('design_fees.html', fees=all_fees)


# --- Ingredient Type Manager ---
@app.route('/ingredient-types', methods=['GET', 'POST'])
def ingredient_types():
    if request.method == 'POST':
        name = request.form.get('name')
        markup = request.form.get('markup')
        if name and markup:
            new_type = models.IngredientType(name=name, markup=float(markup))
            db.session.add(new_type)
            db.session.commit()
            return redirect('/ingredient-types')

    all_types = models.IngredientType.query.all()
    return render_template('ingredient_types.html', types=all_types)

# --- Vendor Manager ---
@app.route('/vendors', methods=['GET', 'POST'])
def vendors():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_vendor = models.Vendor(name=name)
            db.session.add(new_vendor)
            db.session.commit()
            return redirect('/vendors')

        all_vendors = models.Vendor.query.all()
        return render_template('vendors.html', vendors=all_vendors)

# --- Profit Margin Dashboard ---
@app.route('/profit-margins')
def profit_margins():
    return "Profit Margin Dashboard (Step 7)"

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Auto-creates app.db and tables if they don't exist
    app.run(debug=True)


