#!/usr/bin/python3

"""
class BaseModel that defines all common
attributes/methods for other classes
take care of the initialization, serialization and
deserialization of your future instances
"""
from datetime import datetime
import models
from uuid import uuid4


class BaseModel:
    count_instances = 0

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                setattr(self, key, value)
                if key == "created_at":
                    self.created_at = datetime.fromisoformat(value)
                if key == "updated_at":
                    self.updated_at = datetime.fromisoformat(value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

        BaseModel.count_instances += 1

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        new = self.__dict__.copy()
        new["created_at"] = self.created_at.isoformat()
        new["updated_at"] = self.updated_at.isoformat()
        new["__class__"] = self.__class__.__name__
        return new

    def __del__(self):
        BaseModel.count_instances -= 1


