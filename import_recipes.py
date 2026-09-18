import pandas as pd
from app import app
from extensions import db
import models

def import_recipes_from_excel(file_path):
    # 1. Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    with app.app_context():
        # Pre-fetch Products by product_code (case-insensitive) for fast lookup
        products_lookup = {
            p.product_code.strip().lower(): p.id for p in models.Product.query.all()
        }

        # Pre-fetch Ingredients by name (case-insensitive) for fast lookup
        ingredients_lookup = {
            i.name.strip().lower(): i.id for i in models.Ingredient.query.all()
        }

        imported_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            code_val = str(row['Product Code']).strip().lower() if pd.notna(row.get('Product Code')) else None
            ing_val = str(row['Ingredient Name']).strip().lower() if pd.notna(row.get('Ingredient Name')) else None
            
            try:
                quantity = int(row['Quantity']) if pd.notna(row.get('Quantity')) else 1
            except ValueError:
                quantity = 1

            if not code_val or not ing_val:
                print(f"⚠️ Row {index + 2}: Missing Product Code or Ingredient Name. Skipping.")
                skipped_count += 1
                continue

            # Match product_code to Product.id
            product_id = products_lookup.get(code_val)
            if not product_id:
                print(f"⚠️ Row {index + 2}: Product Code '{row.get('Product Code')}' not found in database. Skipping.")
                skipped_count += 1
                continue

            # Match ingredient_name to Ingredient.id
            ingredient_id = ingredients_lookup.get(ing_val)
            if not ingredient_id:
                print(f"⚠️ Row {index + 2}: Stem '{row.get('Ingredient Name')}' not found in database. Skipping.")
                skipped_count += 1
                continue

            # Instantiate ProductIngredient association record
            new_recipe_item = models.ProductIngredient(
                product_id=product_id,
                ingredient_id=ingredient_id,
                quantity=quantity
            )
            db.session.add(new_recipe_item)
            imported_count += 1

        # Commit all recipe records to the database
        db.session.commit()
        print(f"✅ Success! Imported {imported_count} recipe stems ({skipped_count} skipped).")

if __name__ == '__main__':
    # Update 'recipes.xlsx' to your actual file path
    import_recipes_from_excel('recipes.xlsx')