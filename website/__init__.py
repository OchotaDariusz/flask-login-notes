from flask import Flask
from flask_sqlalchemy import SQLAlchemy, inspect
from dotenv import load_dotenv
from os import getenv
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.secret_key = getenv('SECRET_KEY')
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    app.app_context().push()
    create_database(app, User, 'user')
    create_database(app, Note, 'note')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app, model, table_name):
    # CREATE ALL TABLES
    # inspector = inspect(db.engine)
    # print('Creating database...')
    # if not (inspector.has_table('user')) or \
    #         not (inspector.has_table('note')):
    #     db.create_all(app=app)
    #     print('Done')
    # else:
    #     print('Database already exists. Skipping...')
    #
    # CREATE SINGLE TABLES
    # from .models import User, Note
    #
    # inspector = inspect(db.engine)
    # if not (inspector.has_table('user')):
    #     print('Creating database table User...')
    #     User.__table__.create(db.session.bind, checkfirst=True)
    #     print('Done')
    # else:
    #     print('Database already exists. Skipping...')
    #
    # if not (inspector.has_table('note')):
    #     print('Creating database table Note...')
    #     Note.__table__.create(db.session.bind, checkfirst=True)
    #     print('Done')
    # else:
    #     print('Database already exists. Skipping...')

    inspector = inspect(db.engine)
    if not (inspector.has_table(table_name)):
        print(f'Creating database table {table_name}...')
        model.__table__.create(db.session.bind, checkfirst=True)
        print('Done')
    else:
        print('Database already exists. Skipping...')
