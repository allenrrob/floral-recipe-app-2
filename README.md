# Floral Recipe Web App 🌸

A Flask-based web application designed to calculate flower arrangement recipe costs, handle dynamic markup calculations based on ingredient types, apply design fees, calculate profit margins, and suggest retail prices.

---

## 📌 Project Overview & Purpose
This application serves as a complete recipe costing and pricing management system for a floral design business.

### Core Capabilities:
- **Ingredient & Cost Management**: Track raw flower stem/unit costs, colors, and vendor sourcing.
- **Dynamic Markups**: Apply custom markup multipliers categorized by **Ingredient Type** (e.g., standard focal flowers vs. premium imported blooms or hard goods/vases).
- **Design Fee Rules**: Apply automated labor and design percentages based on **Design Type** (e.g., Everyday Arrangement, Funeral Spray, Wedding Floral Package).
- **Recipe Management**: Link multiple ingredients with specific stem/unit quantities to a single product recipe.
- **Suggested Pricing & Margin Analysis**: Calculate wholesale cost, marked-up cost, design fee, profit margins, and recommended retail price dynamically.
- **Quick Estimating**: Calculate price estimates on the fly without saving them as permanent products.

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

## 🚦 Navigation & Page Map

- **Homepage**: Central hub with navigation links to all app modules.
- **Ingredient Page**: Search, filter, add, and edit floral ingredients and unit costs.
- **Product & Recipe Page**: Lookup existing product recipes, edit stem counts, and build new arrangements.
- **Temporary Design Calculator**: Scratchpad calculator to quickly test pricing scenarios without creating permanent database entries.
- **Design Fee Manager**: Set up and edit percentage-based design/labor fees by design classification.
- **Ingredient Type Manager**: Manage ingredient classifications and set their baseline markup multipliers.
- **Profit Margin Analytics**: Review profitability reports and margin percentages across products.
- **Vendor Manager**: Track supplier details, view catalog items per vendor, and generate vendor purchase/ingredient reports.

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
- [x] Updated project roadmap with full navigation architecture and feature specifications.

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

#### Phase 2: Core Costing & Margin Logic
- [ ] Build helper methods on models to calculate:
  - **Raw Wholesale Cost**: `sum(Ingredient.unit_cost * Quantity)`
  - **Marked-up Cost**: `sum(Ingredient.unit_cost * Quantity * IngredientType.markup_multiplier)`
  - **Design Fee**: `Marked-up Cost * DesignType.design_fee_percentage`
  - **Suggested Retail Price**: `Marked-up Cost + Design Fee`
  - **Profit Margin %**: `((Retail Price - Wholesale Cost) / Retail Price) * 100`

#### Phase 3: Route & Template Construction
- [ ] **Homepage**: Build main dashboard with dynamic navigation links.
- [ ] **Ingredient Management**: Search/edit interface and vendor association.
- [ ] **Product & Recipe Manager**: Recipe builder with real-time cost updates.
- [ ] **Temporary Calculator**: Unsaved sandbox for custom quotes.
- [ ] **Fee & Type Managers**: CRUD pages for Design Fees and Ingredient Types.
- [ ] **Vendor Reports Page**: Filter ingredients by supplier and run item lists.
- [ ] **Profit Margin Dashboard**: High-level view of retail price vs. actual margins.

#### Phase 4: UI/UX & SCSS Styling
- [ ] Build global navigation header/sidebar in `base.html`.
- [ ] Style data tables, forms, search inputs, and metric cards using SCSS.

---

## 🐞 Bug Tracker & Known Issues
*No active bugs reported.*

---

## 📝 To-Do List & Backlog
- [ ] Seed initial database with sample floral data (e.g., Roses, Hydrangeas, Vases, Everyday Arrangement Design Fee).
- [ ] Add error handling and flash notifications for form submissions.
- [ ] Optional: Add stem loss / wastage percentage calculation factor to recipes.