from app import db

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship to ingredients provided by this vendor
    ingredients = db.relationship('Ingredient', backref='vendor', lazy=True)

    def __repr__(self):
        return f'<Vendor {self.name}>'

class IngredientType(db.Model):
    __tablename__ = 'ingredient_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True) # e.g. Flower, Filler, Supply
    markup = db.Column(db.Float, default=4.0) # Multiplier

    # Relationship to ingredients of this type
    ingredients = db.relationship('Ingredient', backref='type_info', lazy=True)

    def __repr__(self):
        return f'<IngredientType {self.name}>'

class DesignType(db.Model):
    __tablename__ = 'design_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True) # Default, Simple, Complex, Plant etc.
    design_fee_percentage = db.Column(db.Float, default = 20.00)

    # Relationship to products using this design style
    products = db.relationship('Product', backref='design_style', lazy=True)

    def __repr__(self): 
        return f'<DesignType {self.name}>'

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost_per_pkg = db.Column(db.Float, nullable=False)
    qty_per_pkg = db.Column(db.Float, nullable=False)

    # Foreign Keys
    ingredient_type_id = db.Column(db.Integer, db.ForeignKey('ingredient_types.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)

    def __repr__(self):
        return f'<Ingredient {self.name}>'

class ProductIngredient(db.Model):
    __tablename__ = 'product_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Foreign Keys
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)

    # Relationships to access related objects directly from a recipe row
    ingredient = db.relationship('Ingredient')

    def __repr__(self):
        return f'<ProductIngredient {self.quantity} x {self.ingredient_id}>'

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    product_code = db.Column(db.String(20), nullable=False)
    actual_price = db.Column(db.Float, nullable=True)

    # Foreign Keys
    design_type_id = db.Column(db.Integer, db.ForeignKey('design_types.id'), nullable=False)

    # Relationship to join table
    recipe_items = db.relationship('ProductIngredient', backref='product', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'

    # --- Costing & Pricing Calculations ---
    @property
    def raw_wholesale_cost(self):
        """Calculates total raw/stem unit costs without markups."""
        return sum((item.ingredient.cost_per_pkg / item.ingredient.qty_per_pkg) * item.quantity for item in self.recipe_items)

    @property
    def marked_up_cost(self):
        """Calculates ingredient costs with ingredient-type markkups applied."""
        total = 0.0
        for item in self.recipe_items:
            markup = item.ingredient.type_info.markup if item.ingredient.type_info else 1.0
            total += ((item.ingredient.cost_per_pkg / item.ingredient.qty_per_pkg) * item.quantity) * markup
        return total

    @property
    def design_fee(self):
        """Calculates design fee based on the product's design type percentage."""
        fee_pct = self.design_style.design_fee_percentage if self.design_style else 0.0
        return self.marked_up_cost * (fee_pct / 100.00)

    @property
    def suggested_retail_price(self):
        """Calculates recommended retail price (Marked up cost + Design fee)."""
        return self.marked_up_cost + self.design_fee

    @property
    def profit_margin_percentage(self):
        """Calculates profit margin percentage based on suggested retail price"""
        srp = self.suggested_retail_price
        if srp == 0: 
            return 0.0
        return ((srp - self.raw_wholesale_cost) / srp) * 100.0