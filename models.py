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
