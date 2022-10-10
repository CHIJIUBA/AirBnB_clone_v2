#!/usr/bin/python3
"""
Defines the BaseModel class.
"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represent the base model.

    defines all common attributes/methods for other classes.

    """

    def __init__(self, *args, **kwargs):
        """Initialize a new Base model.

        Args:
            **kwargs (dict): The identity of the new Base.
            *args(any): The identity of the new Base
        """
        if kwargs and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            from models import storage
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return the print() and str() representation the basemodel."""
        return "[{}] ({}) {}".format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        """updates the updated_at with the current datetime."""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return the dictionary representation of the basemodel."""
        dict_1 = self.__dict__.copy()
        dict_1["__class__"] = self.__class__.__name__
        for k, v in self.__dict__.items():
            if k in ("created_at", "updated_at"):
                v = self.__dict__[k].isoformat()
                dict_1[k] = v
        return dict_1
