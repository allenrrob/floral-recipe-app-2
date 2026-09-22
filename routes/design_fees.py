from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
import models

design_fees_bp = Blueprint('design_fees', __name__)

# --- Design Fee Manager ---
@design_fees_bp.route('/design-fees', methods=['GET', 'POST'])
def design_fees():
    if request.method == 'POST':
        action = request.form.get('action')

        # Action: Create a new design fee style
        if action == 'create_design_type' or not action:
            name = request.form.get('name')
            fee_pct = request.form.get('design_fee_percentage')
            if name and fee_pct:
                new_fee = models.DesignType(
                    name=name.strip(), 
                    design_fee_percentage=float(fee_pct)
                )
                db.session.add(new_fee)
                db.session.commit()
                return redirect(url_for('design_fees.design_fees'))

        # Action: Edit an existing design fee style
        elif action == 'edit_design_type':
            dt_id = request.form.get('design_type_id')
            name = request.form.get('name')
            fee_pct = request.form.get('design_fee_percentage')

            if dt_id and name and fee_pct:
                dt = models.DesignType.query.get(int(float(dt_id)))
                if dt:
                    dt.name = name.strip()
                    dt.design_fee_percentage = float(fee_pct)
                    db.session.commit()

            return redirect(url_for('design_fees.design_fees'))

    all_fees = models.DesignType.query.order_by(models.DesignType.name.asc()).all()
    return render_template('design_fees.html', fees=all_fees)