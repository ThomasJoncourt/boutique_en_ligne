from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Customers, Products, Orders, ProductsInOrder
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
#from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/bnp2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

#metrics = PrometheusMetrics(app)

# Ajoutez cette ligne pour exporter automatiquement les métriques par défaut pour Flask
#metrics.register_default()

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Customers.query.get(int(user_id))

# Routes à créer ici (index, register, login, etc.)

@app.route('/')
def index():
    products = Products.query.all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        adress = request.form['adress']
        cp = request.form['cp']
        city = request.form['city']
        
        # Vérifiez si l'utilisateur existe déjà
        user = Customers.query.filter_by(email=email).first()
        if user:
            flash('Cet email est déjà utilisé. Veuillez en utiliser un autre.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_customer = Customers(email=email, first_name=first_name, last_name=last_name, password_=hashed_password, adress=adress, cp=cp, city=city)
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    next_page = request.args.get('next', url_for('index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember_me')
        
        user = Customers.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_, password):
            login_user(user, remember=remember_me)
            session['cart'] = {}  # Initialise le panier
            return redirect(next_page)
        else:
            flash('Identifiants incorrects. Veuillez réessayer.', 'danger')
    
    return render_template('login.html', next=next_page)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Products.query.get(product_id)
    if product:
        cart = session.get('cart') or {} 
        cart[str(product_id)] = cart.get(str(product_id),0) + 1  # Ajoute 1 à la quantité de cet article
        session['cart'] = cart
        flash(f"{product.item} a été ajouté à votre panier", "success")
    else:
        flash("Ce produit n'existe pas", "danger")
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
#@login_required
def cart():
    if request.method == 'POST':
        # Créez la commande pour le client actuel
        order = Orders(id_customer=current_user.id, cash_price=0)
        db.session.add(order)
        db.session.commit()

        # Parcourez les éléments du panier et ajoutez-les à la commande
        cart_items = request.form.getlist('product_id')
        cart_quantities = request.form.getlist('quantity')
        total_price = 0

        for i, product_id in enumerate(cart_items):
            product = Products.query.get(product_id)
            quantity = int(cart_quantities[i])
            total_price += product.price * quantity

            # Ajoutez l'élément de commande à la base de données
            order_item = ProductsInOrder(order_id=order.id, product_id=product_id, quantity=quantity)
            db.session.add(order_item)

        # Mettez à jour le prix total de la commande
        order.cash_price = total_price
        db.session.commit()

        flash("Votre commande a été passée avec succès!", "success")
        return redirect(url_for('index'))

    cart = session.get('cart') or {}
    cart_items = []
    for product_id, quantity in cart.items():
        product = Products.query.get(product_id)
        cart_items.append({'product': product, 'quantity': quantity})  

    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
