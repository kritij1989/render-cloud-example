import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime
import json

DB_HOST=os.getenv('DB_HOST','localhost:5432')
DB_USER=os.getenv('DB_USER','postgres')
DB_PASSWORD=os.getenv('DB_PASSWORD','Nainu1234')
DB_NAME=os.getenv('DB_NAME','castagency')
DB_PATH="postgresql://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD, DB_HOST, DB_NAME)

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    # db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime(), nullable=False)   

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()