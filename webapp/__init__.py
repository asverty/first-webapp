from flask import Flask, render_template, flash, redirect, url_for
from flask_login import current_user, LoginManager, login_required
from flask_login import login_user, logout_user


from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        User.query.get(user_id)

    @app.route('/')
    def index():
        title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template(
            'index.html',
            page_title=title,
            weather=weather,
            news_list=news_list)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('/index'))
        title = 'Authorization'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Welcome')
                return redirect(url_for('index'))
        flash('Incorrect login or pass')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash("You're successfully logout")
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_index():
        return('Hello admin!')

    return app
# if __name__ == "__main__":
#     app.run(debug=True)
