from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from models.database import Categories
from datetime import datetime

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories')
@login_required 
def show_categories():
    categories = Categories.objects()
    return render_template('categories.html', categories=categories)
@login_required
@categories_bp.route('/addcategories')
def addd_categories():
    categories = Categories.objects(Trace__enabled=True)
    return render_template('addCategories.html', categories=categories)

@categories_bp.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    name = request.form['name']
    description = request.form['description']
    traced = {"created": datetime.now(), "updated": datetime.now(), "enabled": True}
    categories = Categories(Name=name, Description=description,Trace=traced)
    categories.save()
    flash("Category added succesfully")
    return redirect('/categories')

@categories_bp.route('/edit/<string:category_id>', methods=['GET', 'POST'])
@login_required
def edit_categories(category_id):
    category = Categories.objects(id=category_id).first()
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        trace = category.Trace
        trace['updated'] = datetime.now()
        category.update(Name=name, Description=description, Trace=trace)

        flash("Category updated successfully")
        return redirect('/categories')

    return render_template('edit_categories.html', category=category)

@categories_bp.route('/delete/<string:category_id>')
@login_required
def delete_category(category_id):
    category = Categories.objects(id=category_id).first()

    if category:
        trace = category.Trace

        trace['enabled'] = False
        category.update(Trace=trace)
        flash("Category deleted successfully")
    else:
        flash("Category not found")

    return redirect('/categories')

@categories_bp.route('/reset/<string:category_id>')
@login_required
def reset_category(category_id):
    category = Categories.objects(id=category_id).first()

    if category:
        trace = category.Trace

        trace['enabled'] = True
        category.update(Trace=trace)
        flash("Category recover successfully")
    else:
        flash("Category not found")

    return redirect('/categories')

@categories_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401

