from flask import Blueprint, render_template
from flask_login import current_user

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    '''For 404 [Not Found] Error'''
    if current_user.is_authenticated:
        back = 'users.home'
    else:
        back = 'main.welcome'
    print(f'Error caught : {error}')
    return render_template('errors/404.html', back=back), 404

@errors.app_errorhandler(403)
def error_403(error):
    '''For 403 [Forbidden Request] Error'''
    print(f'Error caught : {error}')
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    '''For 500 [General] Error'''
    print(f'Error caught : {error}')
    return render_template('errors/500.html'), 500
