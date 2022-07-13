from .local_filestorage import LocalFileStorage
from .mimio_storage import MinioFileStorage


class FilesStorageSystem:

    def __init__(self):
        pass

    system = staticmethod(None)

    @staticmethod
    def get_system():
        if FilesStorageSystem.system is None:
            FilesStorageSystem.system = MinioFileStorage()
        return FilesStorageSystem.system
