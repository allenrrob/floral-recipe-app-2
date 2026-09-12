import os
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from extensions import db

# Floral Recipe App 
app = Flask(__name__)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
Scss(app, static_dir='static', asset_dir='static/scss')

# Import models so SQLAlchemy is aware of them
import models 

# App Routes
# --- Home page ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Ingredient Manager ---
@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    if request.method == 'POST':
        name = request.form.get('name')
        cost_per_pkg = request.form.get('cost_per_pkg')
        qty_per_pkg = request.form.get('qty_per_pkg')
        type_id = request.form.get('ingredient_type_id')
        vendor_id = request.form.get('vendor_id')

        if name and cost_per_pkg and qty_per_pkg and type_id:
            new_ingredient = models.Ingredient(
                name=name,
                cost_per_pkg=float(cost_per_pkg),
                qty_per_pkg=float(qty_per_pkg),
                ingredient_type_id=int(type_id),
                vendor_id=int(vendor_id) if vendor_id else None
            )

            db.session.add(new_ingredient)
            db.session.commit()
            return redirect('/ingredients')

    # Query inventory items along with dropdown choices for foreign keys
    all_ingredients = models.Ingredient.query.all()
    all_types = models.IngredientType.query.all()
    all_vendors = models.Vendor.query.all()

    return render_template(
        'ingredients.html',
        ingredients=all_ingredients,
        types=all_types,
        vendors=all_vendors
    )


# --- Product Manager ---
@app.route('/products', methods=['GET','POST'])
def products():
    if request.method == 'POST':
        action = request.form.get('action')

        # Action 1: Create a new product base
        if action == 'create_product':
            name = request.form.get('name')
            code = request.form.get('product_code')
            design_id = request.form.get('design_type_id')

            if name and code and design_id:
                new_product = models.Product(
                    name=name,
                    product_code=code,
                    design_type_id=int(design_id)
                )
                db.session.add(new_product)
                db.session.commit()

        # Action 2: Add an ingredient stem & quantity to product's recipe
        elif action == 'add_ingredient':
            product_id = request.form.get('product_id')
            ingredient_id = request.form.get('ingredient_id')
            quantity = request.form.get('quantity')

            if product_id and ingredient_id and quantity:
                recipe_item = models.ProductIngredient(
                    product_id=int(product_id),
                    ingredient_id=int(ingredient_id),
                    quantity=int(quantity)
                )
                db.session.add(recipe_item)
                db.session.commit()

        # Action 3: Delete a recipe item from an arrangement
        elif action == 'delete_recipe_item':
            item_id = request.form.get('recipe_item_id')
            if item_id:
                item=models.ProductIngredient.query.get(int(item_id))
                if item:
                    db.session.delete(item)
                    db.session.commit()
        return redirect('/products')

    # Query all products, ingredients, and design fee styles
    all_products = models.Product.query.all()
    all_ingredients = models.Ingredient.query.all()
    all_design_types = models.DesignType.query.all()

    return render_template(
        'products.html',
        products=all_products,
        ingredients=all_ingredients,
        design_types=all_design_types
    )



# --- Quick Calculator ---
@app.route('/temp-calculator')
def temp_calculator():
    return "Quick Design Calculator (Step 7)"

# --- Design Fee Manager ---
@app.route('/design-fees', methods=['GET', 'POST'])
def design_fees():
    if request.method == 'POST':
        name = request.form.get('name')
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