from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Product

main = Blueprint('main', __name__)

@main.route('/')
def home():
    all_products = Product.query.all()
    return render_template('home.html', products=all_products)

@main.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))

@main.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []

    products = Product.query.all()  # ✅ You need this line

    for product in products:
        if query in product.name.lower() or query in product.category.lower():
            results.append(product)

    return render_template('search_results.html', query=query, results=results)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Only admins can add products.")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        description = request.form.get('description')

        new_product = Product(
            name=name,
            category=category,
            price=float(price),
            description=description
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added!')
        return redirect(url_for('main.home'))
    
    # --- EDIT PRODUCT ---
@main.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = request.form['price']
        product.description = request.form['description']

        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for('main.home'))

    return render_template('edit_product.html', product=product)


# --- DELETE PRODUCT ---
@main.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('main.home'))

    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "info")
    return redirect(url_for('main.home'))

    return render_template('add_product.html')