import pandas as pd
from app import app
from extensions import db
import models

def import_vendors_from_excel(file_path):
    df = pd.read_excel(file_path)

    with app.app_context():
        db.create_all()

        imported_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            vendor_name = str(row['Vendor Name']).strip() if pd.notna(row.get('Vendor Name')) else None

            if not vendor_name:
                print(f"⚠️ Row {index + 2}: Missing Vendor Name. Skipping.")
                skipped_count += 1
                continue

            # Check for existing vendor to avoid duplicates
            existing = models.Vendor.query.filter_by(name=vendor_name).first()
            if existing:
                print(f"⚠️ Row {index + 2}: Vendor '{vendor_name}' already exists. Skipping.")
                skipped_count += 1
                continue

            new_vendor = models.Vendor(name=vendor_name)
            db.session.add(new_vendor)
            imported_count += 1

        db.session.commit()
        print(f"✅ Success! Imported {imported_count} vendors ({skipped_count} skipped).")

if __name__ == '__main__':
    import_vendors_from_excel('vendors.xlsx')