from flask import render_template, redirect, url_for, flash, request, Blueprint
from flaskapp import db
from flask_login import current_user
from flaskapp.models import Booking, UserBooking

booking = Blueprint('bookings', __name__)


@booking.route('/bookings')
def bookings():
    bookings = Booking.query.all()
    return render_template('booking.html', page_title='Bookings', user=current_user, bookings=bookings)


@booking.route('/admin/add_booking', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.booking'))

    return render_template('admin/add_booking.html', page_title='Add a Booking', admin_user=current_user)


@booking.route('/admin/update_booking/<int:booking_id>', methods=['GET', 'POST'])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)

    if request.method == 'POST':
        insurance_company = request.form.get('insurance_company')
        insurance_type = request.form.get('insurance_type')
        coverage_details = request.form.get('coverage_details')
        price = request.form.get('price')

        booking.insurance_company = insurance_company
        booking.insurance_type = insurance_type
        booking.coverage_details = coverage_details
        booking.price = price

        db.session.commit()
        flash('Booking has been updated!', category='success')
        return redirect(url_for('admin.booking'))

    return render_template('admin/add_booking.html', page_title='Update a Booking', booking=booking, admin_user=current_user)


@booking.route('/admin/delete_booking/<int:booking_id>', methods=['GET', 'POST'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)

    if booking is not None:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking has been deleted!', category='success')
        return redirect(url_for('admin.booking'))

    else:
        flash('Booking has been deleted!', category='success')
        return redirect(url_for('admin.booking'))


@booking.route('/all_users_bookings')
def all_users_bookings():
    bookings = UserBooking.query.all()
    return render_template('admin/all_users_bookings.html', page_title='List all Bookings', bookings=bookings, admin_user=current_user)
