from flask import Blueprint, render_template, request, redirect 
from extensions import db
import models

vendors_bp = Blueprint('vendors', __name__)

# --- Vendor Manager ---
@vendors_bp.route('/vendors', methods=['GET', 'POST'])
def vendors():
    if request.method == 'POST':
        action = request.form.get('action')

        # Action: Create a new vendor
        if action == 'create_vendor':
            name = request.form.get('name')
            if name:
                new_vendor = models.Vendor(name=name)
                db.session.add(new_vendor)
                db.session.commit()
                return redirect('/vendors')

        elif action == 'edit_vendor':
            vendor_id = request.form.get('vendor_id')
            name = request.form.get('name')

            if vendor_id and name:
                vendor = models.Vendor.query.get(int(vendor_id))
                if vendor:
                    vendor.name = name.strip()

                    db.session.commit()
            return redirect('/vendors')


    all_vendors = models.Vendor.query.order_by(models.Vendor.name.asc()).all()
    return render_template('vendors.html', vendors=all_vendors)