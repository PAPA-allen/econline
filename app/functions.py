import datetime
import os
import secrets
import threading
import time

from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from PIL import Image

from app.decorators import async_call
from app.extensions import db, mail
from app.models import Election


#decorator design pattern
@async_call
def start_end_election():
    elections = Election.query.all()
    for election in elections:
        if election.start_at < datetime.datetime.now() and election.status == "Building":
            election.status = "Ongoing"
            db.session.commit()
        elif election.end_at < datetime.datetime.now():
            election.status = "Ended"
            db.session.commit()
    

def save_picture(candidate_name,form_picture):
    app = current_app._get_current_object()
    with app.app_context():
        random_hex = secrets.token_hex(3)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = candidate_name + random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/candidate_pictures', picture_fn)
        form_picture.save(picture_path)
        
        output_size = (500, 500) #minimizing the size of the image so it isn't saved so large in the database
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        
        return picture_fn


@async_call
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        

def send_mail(to, subject, template):
    app = current_app._get_current_object()
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=('Business House Junior Common Room', 'noreply@sender.com')
    )
    send_async_email(app, msg)
    

def generate_confirmation_token(email):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=864000):
    app = current_app._get_current_object()
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
