from flask import Blueprint, render_template
from flask_login import current_user

errors = Blueprint('errors', __name__)

# For 404 [Not Found] Error
@errors.app_errorhandler(404)
def error_404(error):
    if current_user.is_authenticated:
        back = 'users.home'
    else:
        back = 'main.welcome'
    return render_template('errors/404.html', back=back), 404

# For 403 [Forbidden Request] Error
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# For 500 [General] Error
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500