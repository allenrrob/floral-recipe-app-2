import os
from flask import Flask, render_template, redirect, request, url_for
from flask_scss import Scss
from extensions import db
from sqlalchemy import or_
from routes.ingredients import ingredients_bp
from routes.vendors import vendors_bp
from routes.ingredient_types import ingredient_types_bp
from routes.design_fees import design_fees_bp

# Floral Recipe App 
app = Flask(__name__)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
Scss(app, static_dir='static', asset_dir='static/scss')

app.register_blueprint(ingredients_bp)
app.register_blueprint(vendors_bp)
app.register_blueprint(ingredient_types_bp)
app.register_blueprint(design_fees_bp)

# Import models so SQLAlchemy is aware of them
import models 

# App Routes
# --- Home page ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Product Manager ---
@app.route('/products', methods=['GET','POST'])
def products():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()

    if request.method == 'POST':
        action = request.form.get('action')

        # Action: Create a new product base
        if action == 'create_product':
            name = request.form.get('name')
            code = request.form.get('product_code')
            image_url = request.form.get('image_url')
            actual_price = request.form.get('actual_price')
            design_id = request.form.get('design_type_id')

            if name and code and design_id:
                new_product = models.Product(
                    name=name,
                    product_code=code,
                    image_url=image_url if image_url else None,
                    actual_price=float(actual_price) if actual_price else None,
                    design_type_id=int(design_id)
                )
                db.session.add(new_product)
                db.session.commit()
                return redirect(url_for('products', page=page, q=search_query))

        # Action: Add an ingredient stem & quantity to product's recipe
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
                # Retain search and page params on redirect
                page = request.args.get('page', 1, type=int)
                q = request.args.get('q', '')
                return redirect(url_for('products', page=page, q=q))

        # Action: Delete a recipe item from an arrangement
        elif action == 'delete_recipe_item':
            item_id = request.form.get('recipe_item_id')
            if item_id:
                item=models.ProductIngredient.query.get(int(item_id))
                if item:
                    db.session.delete(item)
                    db.session.commit()
                    page = request.args.get('page', 1, type=int)
                    q = request.args.get('q', '')
                    return redirect(url_for('products', page=page, q=q))

        elif action == 'edit_product':
            product_id = request.form.get('product_id')
            name = request.form.get('name')
            code = request.form.get('product_code')
            actual_price = request.form.get('actual_price')
            image_url = request.form.get('image_url')
            design_id = request.form.get('design_type_id')

            if product_id and name and code and design_id:
                product = models.Product.query.get(int(product_id))
                if product: 
                    product.name = name.strip()
                    product.product_code = code
                    product.actual_price = float(actual_price) if actual_price else None
                    product.image_url = image_url if image_url else None
                    product.design_type_id = int(design_id)
                    db.session.commit()
            return redirect(url_for('products', page=page, q=search_query))

    # GET Request handling (Search + Pagination)
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 25 # Limits display to 25 products per page

    # Base query
    query = models.Product.query
    
    # Apply search filter if query string is present
    if search_query:
        query = query.filter(
            or_(
                models.Product.name.ilike(f'%{search_query}%'),
                models.Product.product_code.ilike(f'%{search_query}%')
            )
        )

    # Execute pagination (returns a Pagination object)
    pagination = query.order_by(models.Product.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Query products on page, all ingredients, and design fee styles
    products_on_page = pagination.items
    all_ingredients = models.Ingredient.query.all()
    all_design_types = models.DesignType.query.all()

    return render_template(
        'products.html',
        products=products_on_page,
        pagination=pagination,
        search_query=search_query,
        ingredients=all_ingredients,
        design_types=all_design_types
    )

# --- Quick Calculator ---
@app.route('/temp-calculator', methods=['GET', 'POST'])
def temp_calculator():
    # Fetch available options for the dropdowns
    all_ingredients = models.Ingredient.query.order_by(models.Ingredient.name.asc()).all()
    all_design_types = models.DesignType.query.order_by(models.DesignType.name.asc()).all()

    # Default results to none and set initial row state
    calculated_results = None
    row_count = 1
    submitted_rows = [('', '1')]
    selected_design_id = None

    if request.method == 'POST':
        action = request.form.get('action')
        current_row_count = int(float(request.form.get('row_count', 1)))

        # Extract selected design style ID and form array inputs
        selected_design_id = request.form.get('design_type_id')
        selected_ing_ids = request.form.getlist('ingredient_id[]')
        quantities = request.form.getlist('quantity[]')

        # Keep track of user entries across re-renders
        submitted_rows = list(zip(selected_ing_ids, quantities))

        # Action: User clicked "+ Add Item"
        if action == 'add_row':
            row_count = current_row_count + 1
            submitted_rows.append(('', '1'))  # Append an empty row pair

        # Action: User clicked a Delete Row button ("delete_row_X")
        elif action and action.startswith('delete_row_'):
            delete_index = int(float(action.split('_')[-1]))
            if 0 <= delete_index < len(submitted_rows):
                submitted_rows.pop(delete_index)
            # Ensure at least 1 row remains visible
            row_count = max(1, len(submitted_rows))

        else:
            row_count = current_row_count

        raw_cost = 0.0
        marked_up_cost = 0.0
        has_items = False

        # Iterate through remaining paired array entries safely
        for ing_id, qty_str in submitted_rows:
            if ing_id and qty_str:
                has_items = True
                qty = float(qty_str)
                ing = models.Ingredient.query.get(int(float(ing_id)))
                if ing and ing.qty_per_pkg > 0:
                    # Calculate single-stem unit cost & markup
                    unit_cost = ing.cost_per_pkg / ing.qty_per_pkg
                    markup = ing.type_info.markup if ing.type_info else 1.0

                    # Accumulate totals across all temporary recipe rows
                    raw_cost += unit_cost * qty
                    marked_up_cost += (unit_cost * qty) * markup

        # Package results if at least one valid item line exists
        if has_items:
            design_style = (
                models.DesignType.query.get(int(float(selected_design_id)))
                if selected_design_id
                else None
            )
            fee_pct = design_style.design_fee_percentage if design_style else 0.0

            design_fee = marked_up_cost * (fee_pct / 100.0)
            srp = marked_up_cost + design_fee
            profit_margin = ((srp - raw_cost) / srp * 100) if srp > 0 else 0.0

            # Package results in a dictionary to pass directly into the template
            calculated_results = {
                'raw_cost': raw_cost,
                'marked_up_cost': marked_up_cost,
                'design_fee': design_fee,
                'srp': srp,
                'margin': profit_margin
            }

    return render_template(
        'temp_calculator.html',
        ingredients=all_ingredients,
        design_types=all_design_types,
        results=calculated_results,
        row_count=row_count,
        submitted_rows=submitted_rows,
        selected_design_id=selected_design_id
    )

# --- Profit Margin Dashboard ---
@app.route('/profit-margins')
def profit_margins():
    # 1. Fetch all products containing their linked recipe items
    products = models.Product.query.all()

    # 2. Aggregate shop-wide financial totals using Python's sum() generator
    total_wholesale = sum(p.raw_wholesale_cost for p in products)
    total_retail = sum(p.suggested_retail_price for p in products)

    # 3. Calculate average margin percentage across all products
    avg_margin = (sum(p.profit_margin_percentage for p in products) / len(products)) if products else 0.0

    return render_template(
        'profit_margins.html',
        products=products,
        total_wholesale=total_wholesale,
        total_retail=total_retail,
        avg_margin=avg_margin
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Auto-creates app.db and tables if they don't exist
    app.run(debug=True)