import os
import secrets

from cyclofit import mail
from flask import current_app, url_for
from flask_mail import Message
from PIL import Image


# To update with uploaded pic
# using _ when not needed
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    folder_directory = os.path.abspath('../CycloFit/cyclofit/pages/static/profile_pics/')
    picture_path = os.path.join(current_app.root_path, folder_directory, picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='cyclofit.noreply.reset@gmail.com',
                recipients=[user.email])
    msg.body = f'''A Password-Change-Request was sent from your account.

To RESET your PASSWORD visit the Link provided and enter your NEW PASSWORD:

{url_for('reset_token', token=token, _external=True)}

Ignore if you did not make the change-request!
'''
    mail.send(msg)
