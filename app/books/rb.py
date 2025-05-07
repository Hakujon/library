class RBBook:
    def __init__(self,
                 id: int | None = None,
                 name: str | None = None,
                 author_id: int | None = None):
        self.id = id
        self.name = name
        self.author_id = author_id

    def to_dict(self):
        data = {"id": self.id, "name": self.name, "author_id": self.author_id}
        filtered_data = {
            key: value for key, value in data.items() if value is not None
            }
        return filtered_data


class RBAuthor:
    def __init__(self,
                 id: int | None = None,
                 first_name: str | None = None,
                 last_name: str | None = None
                 ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        data = {"id": self.id, "first_name": self.first_name, "last_name": self.last_name}
        filtered_data = {
            key: value for key, value in data.items() if value is not None
        }
        return filtered_data