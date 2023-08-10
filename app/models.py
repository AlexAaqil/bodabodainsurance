from app import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    insurance_company = db.Column(db.String, nullable=False)
    insurance_type = db.Column(db.String, nullable=False)
    coverage_details = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)


class UserBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='user_bookings')
    booking = db.relationship('Booking', backref='user_bookings')
