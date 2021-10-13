from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/welcome')
def welcome():
    '''Redirect user to welcome screen'''
    return render_template('welcome.html')
