from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

# USER_CREDENTIALS = {
#     'username': 'tushar',
#     'password': '7290'
# }

@auth_bp.route('/', methods = ["GET", "POST"])
def login(): 
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Fetch user from DB
        user = User.query.filter_by(username=username).first()
        if user and user.username == "admin" :
            user.is_admin = True
            db.session.commit()
       
        if user and user.password == password:
            session['user'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login Successful', 'success')
            return redirect(url_for('tasks.view_tasks'))  # redirect to your tasks page
        else:
            flash('Username or Password not found! Please register.', 'danger')

    return render_template('login.html')



@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists! Please login", "danger")
            return redirect(url_for("auth.register"))
        
        last_user = User.query.order_by(User.display_number.desc()).first()
        next_number = (last_user.display_number + 1) if last_user else 1

        # Create new user
        new_user = User(username=username, password=password, display_number=next_number)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/delete_user/<int:user_id>', methods=["POST"])
def delete_user(user_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if not session.get('is_admin'):
        flash("Only admin can delete users.", "danger")
        return redirect(url_for('tasks.view_tasks'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('auth.view_users'))

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' has been deleted.", "success")

    users = User.query.order_by(User.display_number).all()
    for i, u in enumerate(users, start=1):
        u.display_number = i
    db.session.commit()

    return redirect(url_for('auth.view_users'))


@auth_bp.route('/users')
def view_users():
    if 'user' not in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if not session.get('is_admin'):
        flash("Only admin can view this page.", "danger")
        return redirect(url_for('tasks.view_tasks'))

    users = User.query.all()
    return render_template("users.html", users=users)

