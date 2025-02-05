class BaseModel:
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance