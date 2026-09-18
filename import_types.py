import pandas as pd
from app import app
from extensions import db
import models

def import_types_from_excel(file_path):
    df = pd.read_excel(file_path)

    with app.app_context():
        db.create_all()

        imported_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            type_name = str(row['Type Name']).strip() if pd.notna(row.get('Type Name')) else None
            
            try:
                markup = float(row['Markup']) if pd.notna(row.get('Markup')) else 3.0
            except ValueError:
                markup = 3.0

            if not type_name:
                print(f"⚠️ Row {index + 2}: Missing Type Name. Skipping.")
                skipped_count += 1
                continue

            # Check for existing type
            existing = models.IngredientType.query.filter_by(name=type_name).first()
            if existing:
                print(f"⚠️ Row {index + 2}: Type '{type_name}' already exists. Skipping.")
                skipped_count += 1
                continue

            new_type = models.IngredientType(name=type_name, markup=markup)
            db.session.add(new_type)
            imported_count += 1

        db.session.commit()
        print(f"✅ Success! Imported {imported_count} ingredient types ({skipped_count} skipped).")

if __name__ == '__main__':
    import_types_from_excel('ingredient_types.xlsx')