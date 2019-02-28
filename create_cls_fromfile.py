
import os
import json

class Client(object):
    """
    参考 Scrapy Request类实现
    """

    def __init__(self, callback=None,meta=None,flags=None):
        if callback is not None and not callable(callback):
            raise TypeError('callback must be a callable, got %s' % type(callback).__name__)
        self.callback = callback
        self._meta = dict(meta) if meta else None
        self.flags = [] if flags is None else list(flags)

    @property
    def meta(self):
        if self._meta is None:
            self._meta = {}
        return self._meta

    def copy(self):
        return self.replace()

    def replace(self, *args, **kwargs):
        for x in ['meta','callback', 'flags']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)


class Handler(object):
    def __init__(self, **kwargs):
        self.config = kwargs

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            return cls.from_dict(**json.load(f))

    @staticmethod
    def save_file(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)

    @classmethod
    def from_dict(cls, **kwargs):
        try:
            return cls(**kwargs)
        except TypeError:
            raise ValueError('{} type error'.format(kwargs))

def process(data):
    return data


if __name__ == '__main__':

    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_path,'config','config.json')
    cls = Handler.from_file(config_path)
    print(cls.config)
    cls.save_file(config_path+'.bak',cls.config)
    client = Client(callback=process,meta=cls.config)
    client2 = client.copy()
    data = client2.callback(10)
    print(client2.meta,data)


