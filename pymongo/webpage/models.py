from datetime import datetime

class WebPage():
    id : str
    url :str
    title :str
    description :str
    created :datetime
    keyword : list

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
