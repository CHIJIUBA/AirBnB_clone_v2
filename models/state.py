#!/usr/bin/python3
"""
Defines the State class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models.city import City
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represent a state

    Attributes:
        name (str): The name of the state

    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade='all,delete, delete-orphan')
