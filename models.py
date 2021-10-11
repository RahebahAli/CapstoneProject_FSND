import os
import re
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'movieactors')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER,
                                                  DB_PASSWORD,
                                                  DB_HOST, DB_NAME)

database_path = 'postgresql://postgres:postgres@localhost:5432/movieactors'
database_path = os.getenv('DATABASE_URL')

# To solve the problem of database in heroku: The resource:
# https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to
    have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # add one demo row which is helping in POSTMAN test
    company = Company(
        name='Top'
        )
    movie = Movie(
        title="The Home",
        owner_id=1
        )
    actor = Actor(
        name="Ali",
        age=30
        )

    company.insert()
    movie.insert()
    actor.insert()


class Company(db.Model):
    __tablename__ = 'Company'

    id = db.Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)
    movies = db.relationship('Movie', backref='owner')

    def format(self):
        return {
          'id': self.id,
          'name': self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(Integer, primary_key=True)
    title = Column(String(80), nullable=True)
    owner_id = Column(Integer, ForeignKey('Company.id'))

    def format(self):
        return {
          'id': self.id,
          'title': self.title,
          'owner_id': self.owner_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)
    age = Column(Integer, nullable=False)

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'age': self.age
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
