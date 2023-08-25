from flask import render_template, redirect, url_for, flash, request, Blueprint
from flaskapp import db
from flask_login import current_user
from flaskapp.models import Booking, UserBooking

booking = Blueprint('bookings', __name__)


@booking.route('/bookings')
def bookings():
    bookings = Booking.query.all()
    return render_template('booking.html', page_title='Bookings', user=current_user, bookings=bookings)


@booking.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        insurance_company = request.form.get('insurance_company')
        insurance_type = request.form.get('insurance_type')
        coverage_details = request.form.get('coverage_details')
        price = request.form.get('price')

        new_booking = Booking(insurance_company=insurance_company, insurance_type=insurance_type, coverage_details=coverage_details, price=price)
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking has been added!', category='success')
        return redirect(url_for('bookings.bookings'))

    return render_template('add_booking.html', page_title='Add a Booking', user=current_user)


@booking.route('/all_users_bookings')
def all_users_bookings():
    bookings = UserBooking.query.all()
    return render_template('all_users_bookings.html', page_title='List all Bookings', bookings=bookings, user=current_user)
