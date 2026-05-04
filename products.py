from flask import Blueprint, render_template, redirect, request,flash
from flask_login import login_required  
from datetime import datetime
from models.database import Products, Categories
products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
@login_required
def show_product():
    products = Products.objects()
    categories = Categories.objects(Trace__enabled=True)

    return render_template('products.html', products=products, categories=categories)

@products_bp.route('/addproducts')
@login_required
def addd_product():
    products = Products.objects(Trace__enabled=True)
    categories = Categories.objects(Trace__enabled=True)

    return render_template('addProducts.html', products=products, categories=categories)
@products_bp.route('/product/add', methods=['POST'])
@login_required
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category'] 
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}

    product = Products(Name=name, Description=description, Price=price, Quantity=quantity, Category=category, Trace=traced)
    product.save()
    flash("product added succesfully")
    return redirect('/products')

@products_bp.route('/editproduct/<string:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Products.objects(id=product_id).first()
    category=Categories.objects()
    
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']
        category = request.form['category'] 
        trace = product.Trace
        selected_category = Categories.objects.get(id=category)
        trace['updated'] = datetime.now()
        product.update(Name=name, Description=description, Price=price, Quantity=quantity, Category=selected_category, Trace=trace)

        flash("Product updated successfully")
        return redirect('/products')

    return render_template('edit_product.html', product=product,category=category)

@products_bp.route('/deleteproduct/<string:product_id>')
@login_required
def delete_product(product_id):
    product = Products.objects(id=product_id).first()
    

    if product:
        trace = product.Trace

        trace['enabled'] = False
        product.update(Trace=trace)
        flash("Product deleted successfully")
    else:
        flash("Product not found")

    return redirect('/products')
@products_bp.route('/resetproduct/<string:product_id>')
@login_required
def reset_product(product_id):
    product = Products.objects(id=product_id).first()

    if product:
        trace = product.Trace

        trace['enabled'] = True
        product.update(Trace=trace)
        flash("Product recover successfully")
    else:
        flash("Product not found")

    return redirect('/products')

@products_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401