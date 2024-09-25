import os
import boto3
import requests
from botocore.exceptions import NoCredentialsError
from botocore.config import Config
from cloud_provider import CloudProvider

class AWSProvider(CloudProvider):
    def __init__(self, config):
        s3_config = Config(signature_version='s3v4', region_name=config['region_name'])
        self.s3 = boto3.client('s3', 
                               aws_access_key_id=config['access_key_id'],
                               aws_secret_access_key=config['secret_access_key'],
                               config=s3_config)
        self.bucket_name = config['bucket_name']
        self.expiration = config['signed_url_expires']

    def upload_file(self, file_path, destination):
        try:
            if destination == '':
                destination = file_path
            self.s3.upload_file(file_path, self.bucket_name, destination)
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

    def download_file(self, source, destination, is_signed_url):
        try:
            if destination == '':
                destination = source
            if os.path.isdir(destination):
                destination = os.path.join(destination, source.split('/')[-1])
            if not is_signed_url:
                self.s3.download_file(self.bucket_name, source, destination)
                print("Download Successful")
            else:
                response = self.s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': self.bucket_name,
                                                            'Key': source},
                                                    ExpiresIn=self.expiration)
                get_response = requests.get(response)
                if get_response.status_code == 200:
                    with open(destination, 'wb') as file:
                        file.write(get_response.content)
                        print("Download Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")
    
    def list_files(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append(obj['Key'])
                return files
        except NoCredentialsError:
            print("Credentials not available")
