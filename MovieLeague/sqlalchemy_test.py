from flask import Flask
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://movieleague:movieleague@movieleague.cqcfjfvffon5.eu-west-1.rds.amazonaws.com/movieleagetest"
db = SQLAlchemy(app)


class Example(db.Model):
    __tablename__ = 'example'
    id = Column('id', Integer, primary_key=True)
    data = Column('data', String(255))

    def __init__(self, id, data):
        self.id = id
        self.data = data

