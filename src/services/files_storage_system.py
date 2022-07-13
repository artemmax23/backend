from .local_filestorage import LocalFileStorage


class FilesStorageSystem:

    def __init__(self):
        pass

    system = staticmethod(None)

    @staticmethod
    def get_system():
        if FilesStorageSystem.system is None:
            FilesStorageSystem.system = LocalFileStorage()
        return FilesStorageSystem.system
