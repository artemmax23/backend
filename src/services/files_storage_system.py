import os

from .local_filestorage import LocalFileStorage
from .mimio_storage import MinioFileStorage


class FilesStorageSystem:

    def __init__(self):
        pass

    mode = os.getenv('MODE_STORAGE', 'default')
    system = staticmethod(None)

    @staticmethod
    def get_system():
        if FilesStorageSystem.system is None:
            if FilesStorageSystem.mode == 'default':
                FilesStorageSystem.system = LocalFileStorage()
            elif FilesStorageSystem.mode == 'MINIO':
                FilesStorageSystem.system = MinioFileStorage()
        return FilesStorageSystem.system
