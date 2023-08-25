from flask import render_template, Blueprint
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page_title = 'Home'
    return render_template('home.html', page_title=page_title, user=current_user)


@main.route('/information')
def information():
    page_title = 'Information'
    return render_template('information.html', page_title=page_title, user=current_user)


@main.route('/contact')
def contact():
    page_title = 'Contact'
    return render_template('contact.html', page_title=page_title, user=current_user)