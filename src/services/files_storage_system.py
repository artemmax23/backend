import os

from .local_filestorage import LocalFileStorage
from .mimio_storage import MinioFileStorage
from .storage_interface import StorageInterface


class FilesStorageSystem:

    def __init__(self):
        pass

    mode: str = os.getenv('MODE_STORAGE', 'default')
    system: StorageInterface = staticmethod(None)

    @staticmethod
    def get_system() -> StorageInterface:
        if FilesStorageSystem.system is None:
            if FilesStorageSystem.mode == 'default':
                FilesStorageSystem.system = LocalFileStorage()
            elif FilesStorageSystem.mode == 'MINIO':
                FilesStorageSystem.system = MinioFileStorage()
        return FilesStorageSystem.system
