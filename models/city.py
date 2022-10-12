#!/usr/bin/python3
"""
Defines the City class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """Represent a city

    Attributes:
        state_id (str): The state id.
        name (str): The name of the city

    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    # state_id = ""
    # name = ""
