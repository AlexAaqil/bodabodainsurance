from flask import render_template, redirect, url_for, request, flash, Blueprint
from flaskapp import db
from flaskapp.models import User, UserBooking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Sorry! That email has already been taken!', category='error')
        elif len(username) < 1:
            flash('First name must be more than one character', category='error')
        elif len(email) < 1:
            flash('Last name must be more than one character', category='error')
        elif password1 is not None and len(password1) < 4:
            flash('Password must be at least 4 characters long.')
        elif password2 != password1:
            flash('Passwords don\'t match')
        else:
            new_user = User(national_id=national_id, username=username, email=email, password=generate_password_hash(password2, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now login', category='success')
            return redirect(url_for('users.login'))

    return render_template("register.html", user=current_user)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('bookings.bookings'))
            else:
                flash('Ooops! Something went wrong!', category='error')
        else:
            flash('That user does not exist', category='error')

    return render_template("login.html", user=current_user)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/user_bookings", methods=["GET", "POST"])
def user_bookings():
    if request.method == "POST":
        booking_id = int(request.form.get("booking_id"))
        user_id = current_user.id if current_user.is_authenticated else None
        new_user_booking = UserBooking(user_id=user_id, booking_id=booking_id)
        db.session.add(new_user_booking)
        db.session.commit()
        flash(f'You have successfully booked. An insurance agent will contact you soon to complete the booking process', category='success')
        return redirect(url_for("bookings.bookings"))

    if current_user.is_authenticated:
        user = current_user
        list_user_bookings = UserBooking.query.filter_by(user_id=user.id).all()
        return render_template("user_bookings.html", page_title='User Bookings', list_user_bookings=list_user_bookings, user=current_user)
    else:
        return render_template("user_bookings.html", page_title='User Bookings', list_user_bookings=[], user=current_user)