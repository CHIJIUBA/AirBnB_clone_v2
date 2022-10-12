#!/usr/bin/python3
"""
Defines the State class
"""
from models.base_model import BaseModel
from sqlalchemy import Column, String


class State(BaseModel):
    """Represent a state

    Attributes:
        name (str): The name of the state

    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    # name = ""
