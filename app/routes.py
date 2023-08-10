from flask import Flask, render_template, request, url_for, redirect, flash
from app import app, db
from app.models import User, Booking, UserBooking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/')
def home():
    page_title = 'Home'
    return render_template('home.html', page_title=page_title, user=current_user)

@app.route('/bookings')
def bookings():
    page_title = 'Bookings'
    bookings = Booking.query.all()
    return render_template('booking.html', page_title=page_title, user=current_user, bookings=bookings)

@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    page_title = 'Add a Booking'

    if request.method == 'POST':
        insurance_company = request.form.get('insurance_company')
        insurance_type = request.form.get('insurance_type')
        coverage_details = request.form.get('coverage_details')
        price = request.form.get('price')

        new_booking = Booking(insurance_company=insurance_company, insurance_type=insurance_type, coverage_details=coverage_details, price=price)
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking has been added!', category='success')
        return redirect(url_for('bookings'))

    return render_template('add_booking.html', page_title=page_title, user=current_user)

@app.route("/user_bookings", methods=["GET", "POST"])
def user_bookings():
    page_title = 'User Bookings'

    if request.method == "POST":
        booking_id = int(request.form.get("booking_id"))
        user_id = current_user.id if current_user.is_authenticated else None
        new_user_booking = UserBooking(user_id=user_id, booking_id=booking_id)
        db.session.add(new_user_booking)
        db.session.commit()
        flash(f'You have successfully booked. An insurance agent will contact you soon to complete the booking process', category='success')
        return redirect(url_for("bookings"))

    if current_user.is_authenticated:
        user = current_user
        list_user_bookings = UserBooking.query.filter_by(user_id=user.id).all()
        return render_template("user_bookings.html", page_title=page_title, list_user_bookings=list_user_bookings, user=current_user)
    else:
        return render_template("user_bookings.html", page_title=page_title, list_user_bookings=[], user=current_user)

@app.route('/list_all_bookings')
def list_all_bookings():
    page_title = 'List all Bookings'
    all_bookings = UserBooking.query.all()
    return render_template('list_all_bookings.html', page_title=page_title, all_bookings=all_bookings, user=current_user)

@app.route('/information')
def information():
    page_title = 'Information'
    return render_template('information.html', page_title=page_title, user=current_user)

@app.route('/contact')
def contact():
    page_title = 'Contact'
    return render_template('contact.html', page_title=page_title, user=current_user)

@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))

    return render_template("register.html", user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('bookings'))
            else:
                flash('Ooops! Something went wrong!', category='error')
        else:
            flash('That user does not exist', category='error')

    return render_template("login.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))