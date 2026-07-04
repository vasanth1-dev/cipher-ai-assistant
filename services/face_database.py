import pickle
from pathlib import Path


class FaceDatabase:

    def __init__(self):

        self.file = Path("data/faces/faces.pkl")

        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.save({})

    def load(self):

        with open(self.file, "rb") as f:
            return pickle.load(f)

    def save(self, data):

        with open(self.file, "wb") as f:
            pickle.dump(data, f)

    def add(self, name, embedding):

        data = self.load()

        data[name] = embedding

        self.save(data)

    def all(self):

        return self.load()


face_database = FaceDatabase()