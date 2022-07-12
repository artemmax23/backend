from abc import ABC, abstractmethod


class StorageInterface(ABC):

    @abstractmethod
    def add(self, file, path: str, comment: str) -> str:
        pass

    @abstractmethod
    def delete(self, path: str):
        pass

    @abstractmethod
    def update(self, name: str, path: str, extension: str, old_name: str, old_path: str):
        pass

    @abstractmethod
    def download(self, path: str):
        pass

    @abstractmethod
    def sync(self, db) -> list:
        pass
