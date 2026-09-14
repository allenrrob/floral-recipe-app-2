Markdown# 🌸 Floral Recipe & Costing Web App

A Flask-based web application designed for floral designers and shop owners to track inventory stem costs, manage arrangement recipe formulas, apply category-specific markups and labor fees, and dynamically calculate wholesale costs and suggested retail pricing.

---

## 🛠️ Tech Stack & Extensions

* **Backend**: Python 3.12+, Flask
* **Database & ORM**: SQLite (`app.db`), Flask-SQLAlchemy
* **Styling**: SCSS compiled directly to standard CSS via `Flask-Scss`
* **Templating Engine**: Jinja2 (Layout Inheritance & Scaffolding)
* **Architecture**: Decoupled `extensions.py` pattern (`db = SQLAlchemy()`) to prevent circular imports

---

## 📐 Data Architecture & Schema

The application relies on six core relational models connected through foreign key constraints and join tables:

```text
+------------------+         +------------------+         +-------------------+
|      Vendor      |         |  IngredientType  |         |    DesignType     |
+------------------+         +------------------+         +-------------------+
| id (PK)          |         | id (PK)          |         | id (PK)           |
| name             |         | name             |         | name              |
+--------+---------+         | markup           |         | design_fee_pct    |
         |                   +--------+---------+         +---------+---------+
         | 1                          | 1                           | 1
         |                            |                             |
         | N                          | N                           | N
+--------+----------------------------+---------+         +---------+---------+
|                    Ingredient                 |         |      Product      |
+-----------------------------------------------+         +-------------------+
| id (PK)                                       |         | id (PK)           |
| name                                          |         | name              |
| cost_per_pkg                                  |         | product_code      |
| qty_per_pkg                                   |         | actual_price      |
| vendor_id (FK, optional)                      |         | design_type_id(FK)|
| ingredient_type_id (FK)                       |         +---------+---------+
+-----------------------+-----------------------+                   | 1
                        | 1                                         |
                        |                                           | N
                        | N                                         |
               +--------+-------------------------------------------+
               |               ProductIngredient (Join Table)       |
               +----------------------------------------------------+
               | id (PK)                                            |
               | quantity (stems used in recipe)                    |
               | product_id (FK)                                    |
               | ingredient_id (FK)                                 |
               +----------------------------------------------------+
               
---------------------------------------------------------------------------

🧮 Pricing Engine & FormulasAll cost calculations and suggested retail pricing models run dynamically on the Product model via Python @property decorators:Unit / Stem Wholesale Cost:$$\text{Unit Cost} = \frac{\text{cost\_per\_pkg}}{\text{qty\_per\_pkg}}$$Raw Wholesale Cost (Materials Cost):$$\text{Raw Wholesale Cost} = \sum \left( \text{Unit Cost} \times \text{Quantity Used} \right)$$Marked-Up Material Cost:$$\text{Marked-Up Cost} = \sum \left( \text{Unit Cost} \times \text{Quantity Used} \times \text{IngredientType.markup} \right)$$Design / Labor Fee:$$\text{Design Fee} = \text{Marked-Up Cost} \times \left( \frac{\text{DesignType.design\_fee\_percentage}}{100} \right)$$Suggested Retail Price (SRP):$$\text{Suggested Retail Price} = \text{Marked-Up Cost} + \text{Design Fee}$$Gross Profit Margin %:$$\text{Profit Margin \%} = \left( \frac{\text{Suggested Retail Price} - \text{Raw Wholesale Cost}}{\text{Suggested Retail Price}} \right) \times 100$$📁 Project Directory StructurePlaintextfloral-recipe-app/
├── app.py                  # Main Flask application initialization & routes
├── extensions.py           # Shared database instance (db = SQLAlchemy())
├── models.py                # Database schemas, relationships, & pricing properties
├── seed.py                  # Database seed script for initial lookup data
├── static/
│   ├── css/                # Auto-compiled main.css output
│   └── scss/
│       └── main.scss       # SCSS stylesheets and component rules
└── templates/
    ├── base.html           # Primary layout skeleton & top navigation
    ├── index.html          # Dashboard homepage
    ├── vendors.html        # Vendor manager
    ├── ingredient_types.html # Stem categories & markup manager
    ├── design_fees.html     # Design labor fee manager
    ├── ingredients.html     # Inventory stem cost & package manager
    ├── products.html        # Product arrangement & recipe builder
    ├── temp_calculator.html # Quick scratchpad pricing calculator
    └── profit_margins.html  # Profit margin analytics dashboard
---------------------------------------------------------------------------    
🚦 Core Feature Status
[x] Step 1: Database Schema & Setup (models.py, app.py, extensions.py)

[x] Step 2: Database Seeding (seed.py)

[x] Step 3: Base Navigation & Dashboard (base.html, index.html)

[x] Step 4: Supporting CRUD Managers (vendors.html, ingredient_types.html, design_fees.html, SCSS)

[x] Step 5: Ingredient Manager (ingredients.html & /ingredients route)

[x] Step 6: Product & Recipe Builder (products.html & /products route)

[x] Step 7: Quick Calculator & Analytics (temp_calculator.html & profit_margins.html) 
---------------------------------------------------------------------------
📌 TODO / Future Enhancements
[ ] Add option in quick calculator to "Add New Item" dynamically and default to 1 open row

[ ] Add product photos (always visible on product cards)

[ ] Add ingredient photos (visible on hover over ingredient names)

[ ] Add search/filter functionality for inventory ingredients

[ ] Add search/filter functionality for products & recipes

[ ] Add column sorting capability for the Profit Margin Analytics page