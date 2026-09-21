from flask import Blueprint, render_template, request, redirect
from extensions import db
import models

ingredient_types_bp = Blueprint('ingredient_types', __name__)

# --- Ingredient Type Manager ---
@ingredient_types_bp.route('/ingredient-types', methods=['GET', 'POST'])
def ingredient_types():
    if request.method == 'POST':
        action = request.form.get('action')

        # Action: Create an new ingredient type
        if action == 'create_type':
            name = request.form.get('name')
            markup = request.form.get('markup')
            if name and markup:
                new_type = models.IngredientType(name=name, markup=float(markup))
                db.session.add(new_type)
                db.session.commit()
                return redirect('/ingredient-types')

        # Action: Edit existing ingredient type
        elif action == 'edit_type':
            type_id = request.form.get('type_id')
            name = request.form.get('name')
            markup = request.form.get('markup')

            if type_id and name and markup:
                ing_type = models.IngredientType.query.get(int(type_id))
                if ing_type:
                    ing_type.name = name.strip()
                    ing_type.markup = float(markup)

                    db.session.commit()

            return redirect('/ingredient-types')
        
    all_types = models.IngredientType.query.order_by(models.IngredientType.name.asc()).all()
    return render_template('ingredient_types.html', types=all_types)