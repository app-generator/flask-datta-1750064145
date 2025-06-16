# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Positions(db.Model):

    __tablename__ = 'Positions'

    id = db.Column(db.Integer, primary_key=True)

    #__Positions_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    node_id = db.Column(db.Text, nullable=True)
    lat = db.Column(db.Text, nullable=True)
    lon = db.Column(db.Text, nullable=True)
    altitude = db.Column(db.Text, nullable=True)
    sat_num = db.Column(db.Integer, nullable=True)
    heading = db.Column(db.Text, nullable=True)
    speed = db.Column(db.Text, nullable=True)
    dop = db.Column(db.Text, nullable=True)
    ts = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Positions_FIELDS__END

    def __init__(self, **kwargs):
        super(Positions, self).__init__(**kwargs)


class Messages(db.Model):

    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True)

    #__Messages_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    node_id = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    ts = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Messages_FIELDS__END

    def __init__(self, **kwargs):
        super(Messages, self).__init__(**kwargs)


class Nodes(db.Model):

    __tablename__ = 'Nodes'

    id = db.Column(db.Integer, primary_key=True)

    #__Nodes_FIELDS__
    nickname = db.Column(db.Text, nullable=True)
    team = db.Column(db.Text, nullable=True)
    role = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=True)
    last_seen = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Nodes_FIELDS__END

    def __init__(self, **kwargs):
        super(Nodes, self).__init__(**kwargs)



#__MODELS__END
