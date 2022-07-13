from abc import ABC, abstractmethod


class DBInterface(ABC):

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def one(self, file_id: int):
        pass

    @abstractmethod
    def insert(self, name: str, extension: str,
               size: int, path: str, comment: str):
        pass

    @abstractmethod
    def remove(self, file_id: int):
        pass

    @abstractmethod
    def find(self, path: str):
        pass

    @abstractmethod
    def update(self, file_id: int, name: str,
               path: str, comment: str):
        pass

    @abstractmethod
    def delete_by_path(self, name: str, extension: str, path: str):
        pass
