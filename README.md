# Floral Recipe Web App 🌸

A Flask-based web application designed to calculate flower arrangement recipe costs, handle dynamic markup calculations based on ingredient types, apply design fees, and suggest retail prices.

---

## 📌 Project Overview & Purpose
This application serves as a complete recipe costing and pricing management system for a floral design business. 

### Core Capabilities:
- **Ingredient & Cost Management**: Track raw flower stem/unit costs, colors, and vendor sourcing.
- **Dynamic Markups**: Apply custom markup multipliers categorized by **Ingredient Type** (e.g., standard focal flowers vs. premium imported blooms or hard goods/vases).
- **Design Fee Rules**: Apply automated labor and design percentages based on **Design Type** (e.g., Everyday Arrangement, Funeral Spray, Wedding Floral Package).
- **Recipe Management**: Link multiple ingredients with specific stem/unit quantities to a single product recipe.
- **Suggested Pricing Engine**: Calculate wholesale cost, marked-up cost, design fee, and recommended retail price dynamically.

---

## 🛠️ Tech Stack & Architecture
- **Backend Framework**: Python 3.10+ / Flask
- **ORM & Database**: Flask-SQLAlchemy / SQLite (`instance/app.db`)
- **Styling & UI**: SCSS (compiled via `Flask-Scss`) & HTML5
- **Version Control**: Git & GitHub

---

## 📂 Project Structure
```text
floral-recipe-app/
│
├── .venv/                      # Python virtual environment (ignored in Git)
├── instance/                   # Local SQLite database location (ignored in Git)
│   └── app.db
├── static/
│   ├── css/                    # Compiled CSS output (ignored in Git)
│   │   └── main.css
│   └── scss/                   # Source stylesheets
│       └── main.scss
├── templates/                  # Jinja2 HTML templates
│   └── base.html
├── .gitignore                  # Git ignore definitions
├── app.py                      # Main application entry point & setup
├── README.md                   # Project documentation & tracker
└── requirements.txt            # Python dependency freeze
```

---

## 🚦 Project Status & Progress Tracker

### 🟢 Completed Steps
- [x] Initialized Python `.venv` virtual environment in VSCode.
- [x] Installed base dependencies (`Flask`, `Flask-SQLAlchemy`, `Flask-Scss`).
- [x] Generated `requirements.txt` via `pip freeze`.
- [x] Initialized Git repository and set up `.gitignore` to protect virtual environments and databases.
- [x] Configured `app.py` with Flask instance, SQLite URI, and SCSS compilation.
- [x] Created initial base template (`templates/base.html`) and SCSS stylesheet (`static/scss/main.scss`).
- [x] Connected local repository to GitHub.

---

### 🟡 Current Focus
- [ ] Define **SQLAlchemy Database Models** (`Vendor`, `IngredientType`, `DesignType`, `Ingredient`, `Product`, `ProductIngredient`).
- [ ] Implement database initialization scripts (`db.create_all()`).

---

### 🔵 Next Projected Steps

#### Phase 1: Database Schema & Models
- [ ] Write `Vendor` model (Name, Contact Info, Account #).
- [ ] Write `IngredientType` model (Name, Default Markup Multiplier).
- [ ] Write `DesignType` model (Name, Design Fee % / Labor Multiplier).
- [ ] Write `Ingredient` model (Name, Unit Cost, Color, Foreign Keys to `IngredientType` & `Vendor`).
- [ ] Write `Product` model (Name, Description, Target Retail Price, Foreign Key to `DesignType`).
- [ ] Write `ProductIngredient` / Recipe Join Table (Product ID, Ingredient ID, Quantity required).

#### Phase 2: Pricing Logic & Formulas
- [ ] Build helper methods on `Product` to calculate:
  - **Raw Wholesale Cost**: `sum(Ingredient.unit_cost * Quantity)`
  - **Marked-up Cost**: `sum(Ingredient.unit_cost * Quantity * IngredientType.markup_multiplier)`
  - **Design Fee**: `Marked-up Cost * DesignType.design_fee_percentage`
  - **Suggested Retail Price**: `Marked-up Cost + Design Fee`

#### Phase 3: CRUD Routes & Views
- [ ] Create management forms and views for **Vendors**, **Ingredient Types**, and **Design Types**.
- [ ] Create management forms and views for **Ingredients**.
- [ ] Build **Recipe Builder UI** to add/remove ingredients and live-calculate costs for a **Product**.

#### Phase 4: UI/UX & Styling
- [ ] Style application navigation, data tables, and forms using custom SCSS variables.
- [ ] Add printable recipe cost sheets for florists/designers.

---

## 🐞 Bug Tracker & Known Issues
*No active bugs reported.*

---

## 📝 To-Do List & Backlog
- [ ] Seed initial database with sample floral data (e.g., Roses, Hydrangeas, Vases, Everyday Arrangement Design Fee).
- [ ] Add error handling and flash notifications for form submissions.
- [ ] Optional: Add stem loss / wastage percentage calculation factor to recipes.