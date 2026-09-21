from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
import models

ingredients_bp = Blueprint('ingredients', __name__)

# --- Ingredient Manager ---
@ingredients_bp.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()

    if request.method == 'POST':
        action = request.form.get('action')

        # Action: Create a new ingredient
        if action == 'create_ingredient':
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
                return redirect(url_for('ingredients.ingredients', page=page, q=search_query))

        # Action: Edit ingredient
        elif action == 'edit_ingredient':
            ing_id = request.form.get('ingredient_id')
            name = request.form.get('name')
            cost_per_pkg = request.form.get('cost_per_pkg')
            qty_per_pkg = request.form.get('qty_per_pkg')
            type_id = request.form.get('ingredient_type_id')
            vendor_id = request.form.get('vendor_id')

            if ing_id and name and cost_per_pkg and qty_per_pkg:
                ingredient = models.Ingredient.query.get(int(ing_id))
                if ingredient:
                    ingredient.name = name.strip()
                    ingredient.cost_per_pkg = float(cost_per_pkg)
                    ingredient.qty_per_pkg = float(qty_per_pkg)
                    ingredient.ingredient_type_id = int(type_id) if type_id else None
                    ingredient.vendor_id = int(vendor_id) if vendor_id else None

                    db.session.commit()

            return redirect(url_for('ingredients.ingredients', page=page, q=search_query))

    # GET Request Handling
    per_page = 25
    query = models.Ingredient.query

    if search_query:
        query=query.filter(models.Ingredient.name.ilike(f'%{search_query}%'))

    pagination = query.order_by(models.Ingredient.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'ingredients.html',
        ingredients=pagination.items,
        pagination=pagination,
        search_query=search_query,
        vendors=models.Vendor.query.order_by(models.Vendor.name.asc()).all(),
        types=models.IngredientType.query.order_by(models.IngredientType.name.asc()).all()
    )