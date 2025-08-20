from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Product
from app.forms import RegistrationForm, LoginForm, ProductForm, UpdateProfileForm

main = Blueprint('main', __name__)

# ==========================
# Utility Functions
# ==========================
def init_cart():
    if 'cart' not in session:
        session['cart'] = []

# ==========================
# Home & Product Pages
# ==========================
@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)

# ==========================
# User Authentication
# ==========================
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.signup'))

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# ==========================
# Admin Panel & Product Management
# ==========================
@main.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for('main.home'))
    products = Product.query.all()
    return render_template('admin.html', products=products)

@main.route('/addproduct', methods=['GET', 'POST'])
@login_required
def addproduct():
    if not current_user.is_admin:
        flash("You are not authorized.", "danger")
        return redirect(url_for('main.home'))

    form = ProductForm()
    if form.validate_on_submit():
        file = form.image.data
        if file:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            filepath = f"uploads/{filename}"
        else:
            filepath = "uploads/placeholder.png"

        product = Product(name=form.name.data, price=form.price.data,
                          description=form.description.data, image=filepath)
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('main.admin'))

    return render_template('addproduct.html', form=form)

@main.route("/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash("You are not authorized to perform this action.", "danger")
        return redirect(url_for("main.admin"))

    product = Product.query.get_or_404(product_id)
    # Delete image file if exists
    if product.image:
        image_path = os.path.join("app", "static", "uploads", product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    flash(f"Product '{product.name}' has been deleted.", "success")
    return redirect(url_for("main.admin"))

# ==========================
# Cart & Checkout
# ==========================
@main.route('/addtocart/<int:product_id>')
@login_required
def addtocart(product_id):
    init_cart()
    product = Product.query.get_or_404(product_id)
    # Increase quantity if exists
    for item in session['cart']:
        if item['id'] == product.id:
            item['quantity'] += 1
            break
    else:
        session['cart'].append({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': 1})

    session.modified = True
    flash(f"Added {product.name} to cart.", "success")
    return redirect(url_for('main.cart'))

@main.route('/cart')
def cart():
    init_cart()
    cart_items = session['cart']
    grand_total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)

@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    init_cart()
    cart_items = session['cart']
    grand_total = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        # Optionally save order details
        session['cart'] = []
        flash("Order placed successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template('checkout.html', cart_items=cart_items, grand_total=grand_total)

# ==========================
# User Profile
# ==========================
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Profile image upload
        if form.profile_image.data:
            image_file = form.profile_image.data
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_file.filename)
            image_file.save(image_path)
            current_user.profile_image = image_file.filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    # Pre-fill form
    form.username.data = current_user.username
    form.email.data = current_user.email

    # Dummy orders
    orders = [{'id': 101, 'item': 'Pen', 'status': 'Delivered', 'amount': '$10'},
              {'id': 102, 'item': 'Notebook', 'status': 'Pending', 'amount': '$15'}]

    return render_template('profile.html', user=current_user, form=form, orders=orders)
