import pandas as pd
from app import app
from extensions import db
import models

def import_ingredients_from_excel(file_path):
    # 1. Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    with app.app_context():
        # Pre-fetch all types and vendors into lookup dictionaries for fast ID matching
        types_lookup = {t.name.strip().lower(): t.id for t in models.IngredientType.query.all()}
        vendors_lookup = {v.name.strip().lower(): v.id for v in models.Vendor.query.all()}

        imported_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            # Extract and clean row values
            stem_name = str(row['Name']).strip() if pd.notna(row.get('Name')) else None
            type_name = str(row['Type']).strip().lower() if pd.notna(row.get('Type')) else None
            vendor_name = str(row['Vendor']).strip().lower() if pd.notna(row.get('Vendor')) else None
            
            cost_per_pkg = float(row['Cost Per Pkg']) if pd.notna(row.get('Cost Per Pkg')) else 0.0
            qty_per_pkg = int(row['Qty Per Pkg']) if pd.notna(row.get('Qty Per Pkg')) else 1

            if not stem_name:
                continue

            # Match type name to foreign key ID
            type_id = types_lookup.get(type_name)
            if not type_id:
                print(f"⚠️ Warning: Type '{row.get('Type')}' for stem '{stem_name}' not found in database. Skipping row.")
                skipped_count += 1
                continue

            # Match vendor name to foreign key ID (optional)
            vendor_id = vendors_lookup.get(vendor_name) if vendor_name else None

            # Instantiate new Ingredient record
            new_ingredient = models.Ingredient(
                name=stem_name,
                cost_per_pkg=cost_per_pkg,
                qty_per_pkg=qty_per_pkg,
                ingredient_type_id=type_id,
                vendor_id=vendor_id
            )
            db.session.add(new_ingredient)
            imported_count += 1

        # Commit all new records to the database
        db.session.commit()
        print(f"✅ Success! Imported {imported_count} ingredients ({skipped_count} skipped).")

if __name__ == '__main__':
    # Update 'ingredients.xlsx' to your actual file path
    import_ingredients_from_excel('ingredients.xlsx')