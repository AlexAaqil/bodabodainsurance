from flask import render_template, redirect, url_for, request, flash, Blueprint
from flaskapp import db
from flaskapp.models import Admin, Booking, UserBooking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


admin = Blueprint('admin', __name__)

@admin.route('/admin')
def home():
    return render_template('admin/index.html', page_title='Home | Admin', admin_user=current_user)


@admin.route('/admin/information')
def information():
    page_title = 'Information'
    return render_template('admin/information.html', page_title=page_title, admin_user=current_user)


@admin.route('/admin/booking')
def booking():
    bookings = Booking.query.all()
    return render_template('admin/booking.html', page_title='Available Bookings', bookings=bookings, admin_user=current_user)


@admin.route('/admin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Admin.query.filter_by(username=username).first()
        if user:
            flash('Sorry! That email has already been taken!', category='error')
        elif len(username) < 1:
            flash('User name must be more than one character', category='error')
        elif len(email) < 1:
            flash('Wmail must be more than one character', category='error')
        elif password1 is not None and len(password1) < 4:
            flash('Password must be at least 4 characters long.')
        elif password2 != password1:
            flash('Passwords don\'t match')
        else:
            new_user = Admin(username=username, email=email, password=generate_password_hash(password2, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Admin account has been created! You can now login', category='success')
            return redirect(url_for('admin.login'))

    return render_template("admin/register.html", admin_user=current_user)

@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin_user = Admin.query.filter_by(username=username).first()
        if admin_user:
            if check_password_hash(admin_user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(admin_user, remember=True)
                return redirect(url_for('admin.booking'))
            else:
                flash('Ooops! Something went wrong!', category='error')
        else:
            flash('That user does not exist', category='error')

    return render_template("admin/login.html", admin_user=current_user)

@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
