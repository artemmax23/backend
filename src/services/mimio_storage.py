import boto3
import datetime
import json
import os
import io
from werkzeug.utils import secure_filename

from .storage_interface import StorageInterface


class MinioFileStorage(StorageInterface):

    def __init__(self):
        self.session = boto3.Session(profile_name=os.getenv('PROFILE_NAME', 'default'))
        self.s3 = self.session.client(
            's3',
            endpoint_url=os.getenv('BOTO_URL')
        )
        self.default_file_bucket = os.getenv('BOTO_DEFAULT_BUCKET', 'default')
        try:
            self.s3.head_bucket(Bucket=self.default_file_bucket)
        except BaseException:
            self.s3.create_bucket(Bucket=self.default_file_bucket)

    def add(self, file, path: str) -> str:
        self.s3.upload_fileobj(file, self.default_file_bucket, path)
        return path

    def delete(self, file):
        self.s3.delete_object(
            Bucket=self.default_file_bucket,
            Key=file.path
        )

    def update(self, name: str, path: str, extension: str, old_name: str, old_path: str) -> str:
        copy_source: dict = {
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

    def download(self, name: str, extension: str, path: str) -> io.BytesIO:
        file = io.BytesIO()
        self.s3.download_fileobj(
            self.default_file_bucket,
            path,
            file
        )
        return file

    def sync(self, all: str) -> list:
        result: list = json.loads(all)
        db_paths: list = [p['path'] for p in result]

        insert_list: list = []

        for p in self.s3.list_objects(Bucket=self.default_file_bucket)['Contents']:
            if p['Key'] in db_paths:
                db_paths.remove(p['Key'])
            else:
                fullname: list = []
                if p['Key'].count('.') != 0:
                    fullname = p['Key'].split('.')
                else:
                    fullname[0] = p['Key']
                    fullname[1] = ''
                insert_list.append(
                    {'name': fullname[0], 'extension': fullname[1], 'size': p['Size'],
                     'path': p['Key'], 'comment': ""})

        delete_list: list = []

        for p in db_paths:
            file: list = list(filter(lambda x: x['path'] == p, result))
            delete_list.append({'name': file[0]['name'], 'extension': file[0]['extension'], 'path': p})

        return insert_list, delete_list
