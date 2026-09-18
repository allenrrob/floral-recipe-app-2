import pandas as pd
from app import app
from extensions import db
import models

def import_design_types_from_excel(file_path):
    df = pd.read_excel(file_path)

    with app.app_context():
        db.create_all()

        imported_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            name = str(row['Name']).strip() if pd.notna(row.get('Name')) else None
            
            try:
                fee_pct = float(row['Design Fee Percentage']) if pd.notna(row.get('Design Fee Percentage')) else 20.0
            except ValueError:
                fee_pct = 20.0

            if not name:
                print(f"⚠️ Row {index + 2}: Missing Design Type Name. Skipping.")
                skipped_count += 1
                continue

            # Check for existing design type to prevent duplicates
            existing = models.DesignType.query.filter_by(name=name).first()
            if existing:
                print(f"⚠️ Row {index + 2}: Design Type '{name}' already exists. Skipping.")
                skipped_count += 1
                continue

            new_design_type = models.DesignType(name=name, design_fee_percentage=fee_pct)
            db.session.add(new_design_type)
            imported_count += 1

        db.session.commit()
        print(f"✅ Success! Imported {imported_count} design types ({skipped_count} skipped).")

if __name__ == '__main__':
    import_design_types_from_excel('design_types.xlsx')