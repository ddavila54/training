from datetime import datetime

from app.utility.base_object import BaseObject


class Flag(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    @property
    def completed(self):
        return self._completed

    @property
    def completed_ts(self):
        return self._completed_ts

    @completed.setter
    def completed(self, v):
        self._completed = v
        self._completed_ts = datetime.now()

    @property
    def display(self):
        return dict(number=self.number, name=self.name, challenge=self.challenge, completed=self.completed,
                    extra_info=self.extra_info,
                    completed_ts=self.completed_ts.strftime('%Y-%m-%d %H:%M:%S') if self.completed_ts else '')

    def __init__(self, number, name, challenge, extra_info, verify):
        super().__init__()
        self.number = number
        self.name = name
        self.challenge = challenge
        self.extra_info = extra_info
        self.verify = verify
        self._completed = False
        self._completed_ts = None

    def store(self, ram):
        existing = self.retrieve(ram['flags'], self.unique)
        if not existing:
            ram['flags'].append(self)
            return self.retrieve(ram['flags'], self.unique)
        return existing
