from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()
with app.app_context():
    username = input('Enter your login: ')

    if User.query.filter(User.username == username).count():
        print('Login is already exist!')
        sys.exit(0)
    password1 = getpass('Enter your pass: ')
    password2 = getpass('Repeat your pass: ')

    if not password1 == password2:
        print('Incorrect pass, try again')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Create new profile, your ID: {} added.'.format(new_user.id))
