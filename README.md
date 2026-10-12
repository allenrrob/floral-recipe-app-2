# 🌸 Floral Recipe & Cost Management App

A Flask-based web application designed for retail florists to manage stem inventory, construct arrangement recipes, automatically calculate wholesale costs, apply category markups and labor fees, and generate suggested retail prices (SRP).

---

## 🛠️ Tech Stack

* **Backend:** Python 3.12, Flask, Flask-SQLAlchemy (SQLite)
* **Frontend:** Jinja2 Templates, Vanilla JavaScript, Tom-Select (Searchable Dropdowns)
* **Styling:** SCSS compiled to CSS via Dart Sass / `flask-scss`

---

## 🗄️ Database Architecture

The application uses six core relational models to track inventory, pricing, and arrangement composition:

1. **`Vendor`**: Supplier information (`id`, `name`).
2. **`IngredientType`**: Category markups (`id`, `name`, `markup` multiplier float, e.g., `3.5`).
3. **`DesignType`**: Labor/design style fees (`id`, `name`, `design_fee_percentage` float, e.g., `20.0`).
4. **`Ingredient`**: Stems and supplies (`id`, `name`, `cost_per_pkg`, `qty_per_pkg`, `ingredient_type_id`, `vendor_id`).
   * *Calculated:* Unit Cost = `cost_per_pkg / qty_per_pkg`
5. **`Product`**: Arrangement bases (`id`, `name`, `product_code`, `actual_price`, `image_url`, `design_type_id`).
   * *Calculated Metrics:* Raw Wholesale Cost, Marked-Up Cost, Design Fee, Suggested Retail Price (SRP), Profit Margin %.
6. **`ProductIngredient`**: Recipe join table (`id`, `product_id`, `ingredient_id`, `quantity` float).

---

## 🏗️ Project Structure

```text
floral-recipe-app/
├── app.py                 # Application factory & Blueprint registration
├── extensions.py          # Isolated SQLAlchemy database instance (db)
├── models.py              # Database models & pricing calculation logic
├── static/
│   ├── css/
│   │   └── main.css       # Compiled CSS
│   └── scss/
│       └── main.scss      # Main SCSS styles
├── templates/             # Jinja2 template views
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── ingredients.html
│   ├── vendors.html
│   ├── ingredient_types.html
│   ├── design_fees.html
│   └── temp_calculator.html
└── routes/                # Modular Flask Blueprints
    ├── __init__.py
    ├── ingredients.py
    ├── products.py
    ├── vendors.py
    ├── ingredient_types.py
    ├── design_fees.py
    └── calculator.py