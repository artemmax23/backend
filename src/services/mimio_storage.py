import boto3
import datetime
import json
import os
import io
from werkzeug.utils import secure_filename

from .storage_interface import StorageInterface


class MinioFileStorage(StorageInterface):

    def __init__(self):
        self.session = boto3.Session(profile_name='default')
        self.s3 = self.session.client(
            's3',
            endpoint_url='http://minio:9000'
        )
        self.default_file_bucket = os.getenv('BOTO_DEFAULT_BUCKET')
        if not self.s3.head_bucket(Bucket=self.default_file_bucket):
            self.s3.create_bucket(Bucket=self.default_file_bucket)

    def add(self, file, path: str) -> str:
        self.s3.upload_fileobj(file, self.default_file_bucket, path)
        return path

    def delete(self, file):
        self.s3.delete_object(
            Bucket=self.default_file_bucket,
            Key=file.path
        )

    def update(self, name: str, path: str, extension: str, old_name: str, old_path: str) -> dict:
        copy_source = {
                'Bucket': self.default_file_bucket,
                'Key': old_path
            }

        if path != "":
            self.s3.copy_object(
                Bucket=self.default_file_bucket,
                CopySource=copy_source,
                Key=path
            )

            self.s3.delete_object(
                Bucket=self.default_file_bucket,
                Key=old_path
            )
            return path

        return old_path

    def download(self, name: str, extension: str, path: str):
        file = io.BytesIO()
        self.s3.download_fileobj(
            self.default_file_bucket,
            path,
            file
        )
        return file

    def sync(self, all: str) -> list:
        # result = json.loads(all)
        # db_paths = [UPLOAD_FOLDER + p['path'] + p['name'] + '.' + p['extension'] for p in result]
        # cnt = UPLOAD_FOLDER.count('/')
        #
        # insert_list = []
        #
        # for address, dirs, files in os.walk(UPLOAD_FOLDER):
        #     for name in files:
        #         path = os.path.join(address, name)
        #         path = path.replace('\\', '/')
        #         address = address.replace('\\', '/')
        #         if not (path in db_paths):
        #             filename = name.split('.')
        #             info = os.stat(path)
        #             relative = address.split('/', cnt)[cnt]
        #             if len(relative) != 0:
        #                 relative = '/' + relative + '/'
        #             insert_list.append(
        #                 {'name': filename[0], 'extension': filename[1], 'size': info[6], 'path': relative,
        #                  'comment': ""})
        #         else:
        #             db_paths.remove(path)
        #
        # delete_list = []
        # cnt += 1
        #
        # for p in db_paths:
        #     relative = p.split('/', cnt)
        #     relative.reverse()
        #     if relative[0].count('/') != 0:
        #         fullname, path = relative[0][::-1].split('/', 1)
        #         path = path[::-1]
        #         fullname = fullname[::-1]
        #         path = '/' + path + '/'
        #     else:
        #         fullname = relative[0]
        #         path = '/'
        #
        #     if (os.path.exists(UPLOAD_FOLDER + path)) and len(os.listdir(UPLOAD_FOLDER + path)) == 0:
        #         os.removedirs(UPLOAD_FOLDER + path)
        #
        #     name, extension = fullname.split('.', 1)
        #     delete_list.append({'name': name, 'extension': extension, 'path': path})
        #
        # return insert_list, delete_list
        pass
