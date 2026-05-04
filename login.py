from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, current_user,login_required, logout_user
from models.models import User  

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(current_user.get_id())
        flash('You are already logged in', 'info')
        return redirect('/categories')  
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get(username)

        if user:   
            if user.check_password(password):
                print("password correcto")
                login_user(user)
                return redirect('/categories')

            else:
                print("password incorrecto")
                flash('Incorrect credentials', 'error')
                return redirect('/categories')
                
            
        else:
            flash('Incorrect credentials', 'error')

    return render_template('login.html')


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect('/categories')