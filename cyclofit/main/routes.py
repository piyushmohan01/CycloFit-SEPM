from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/welcome')
def welcome():
    return render_template('welcome.html')
