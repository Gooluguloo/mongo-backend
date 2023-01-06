from datetime import datetime

class Webpage():
    url : str
    title : str
    description : str
    created : datetime

    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description
        self.created = datetime.now

    def __repr__(self):
        return self.url

    @property
    def serialized(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'created': self.created,
        }



class Keyword():
    text: str
    total_frequency: int
    entries: list

    def __init__(self, text, total_frequency):
        self.text = text
        self.total_frequency = total_frequency
        self.entries = []

    def __repr__(self):
        return self.text

    @property
    def serialized(self):
        return {
            'text': self.text,
            'entries': dumpsself.entries,
            'total_frequency': self.total_frequency,
        }
