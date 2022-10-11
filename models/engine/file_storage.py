#!/usr/bin/python3
"""
Module file_storage serializes and
deserializes JSON types
"""

import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """
    Custom class for file storage
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns dictionary representation of all objects
        """
        return self.__objects
    
    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        cls_name = cls.__name__
        dct = {}
        for key in self.__objects.keys():
            if key.split('.')[0] == cls_name:
                dct[key] = self.__objects[key]
        return dct

    def new(self, object):
        """sets in __objects the object with the key
        <object class name>.id

        Args:
            object(obj): object to write

        """
        str1 = object.__class__.__name__
        str2 = str(object.id)
        self.__objects[str1 + '.' + str2] = object

    def save(self):
        """
        serializes __objects to the JSON file
        (path: __file_path)
        """
        with open(self.__file_path, 'w+') as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()
                       }, f)
    
    def delete(self, obj=None):
        ''' deletes the object obj from the attribute
            __objects if it's inside it
        '''
        if obj is None:
            return
        obj_key = obj.to_dict()['__class__'] + '.' + obj.id
        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]

    def reload(self):
        """
        deserializes the JSON file to __objects, if the JSON
        file exists, otherwise nothing happens)
        """
        try:
            with open(self.__file_path, 'r') as f:
                dict = json.loads(f.read())
                for value in dict.values():
                    cls = value["__class__"]
                    self.new(eval(cls)(**value))
        except Exception:
            pass
