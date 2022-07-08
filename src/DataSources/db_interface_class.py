from abc import ABC, abstractmethod

class DBInterface(ABC):

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def one_info(self, file_id):
        pass

    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def remove(self, file_id):
        pass

    @abstractmethod
    def find(self, path):
        pass

    @abstractmethod
    def update(self, file_id, data):
        pass

    @abstractmethod
    def get_path(self, file_id):
        pass

    @abstractmethod
    def delete_by_path(self, path):
        pass