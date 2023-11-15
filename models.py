from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    code_ = db.Column(db.String(255), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password_ = db.Column(db.String(255), nullable=False)
    adress = db.Column(db.String(255), nullable=False)
    cp = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    def get_id(self):
        return str(self.id)
    def is_authenticated(self):
        return True

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_customer = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    date_ = db.Column(db.Date, nullable=False)
    cash_price = db.Column(db.Float, nullable=False)

class ProductsInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
