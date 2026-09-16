import pandas as pd
from app import app
from extensions import db
import models

def import_products_from_excel(file_path):
    # 1. Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    with app.app_context():
        # Pre-fetch all design types into a lookup dictionary for fast ID matching
        design_types_lookup = {d.name.strip().lower(): d.id for d in models.DesignType.query.all()}
        
        # Fallback design type if none is provided or matched (uses the first available DesignType)
        default_design_type = models.DesignType.query.first()
        default_design_id = default_design_type.id if default_design_type else 1

        imported_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            name = str(row['Name']).strip() if pd.notna(row.get('Name')) else None
            product_code = str(row['Product Code']).strip() if pd.notna(row.get('Product Code')) else None
            image_url = str(row['Image URL']).strip() if pd.notna(row.get('Image URL')) else None
            
            # Extract actual_price
            actual_price = float(row['Actual Price']) if pd.notna(row.get('Actual Price')) else None
            
            # Extract Design Type name and match to Foreign Key ID
            design_type_name = str(row['Design Type']).strip().lower() if pd.notna(row.get('Design Type')) else None
            design_type_id = design_types_lookup.get(design_type_name, default_design_id)

            if not name or not product_code:
                print(f"⚠️ Row {index + 1}: Missing Name or Product Code. Skipping row.")
                skipped_count += 1
                continue

            # Check if product code already exists to prevent duplicates
            existing_product = models.Product.query.filter_by(product_code=product_code).first()
            if existing_product:
                print(f"⚠️ Skipping duplicate product code: {product_code}")
                skipped_count += 1
                continue

            # Instantiate new Product record
            new_product = models.Product(
                name=name,
                product_code=product_code,
                image_url=image_url if image_url else None,
                actual_price=actual_price,
                design_type_id=design_type_id
            )
            db.session.add(new_product)
            imported_count += 1

        # Commit all new records to the database
        db.session.commit()
        print(f"✅ Success! Imported {imported_count} products ({skipped_count} skipped).")

if __name__ == '__main__':
    # Update 'products.xlsx' to your actual file path
    import_products_from_excel('products.xlsx')