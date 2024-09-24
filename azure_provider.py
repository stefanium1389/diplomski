import os
import requests
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from cloud_provider import CloudProvider

class AzureProvider(CloudProvider):
    
    def __init__(self, config):
        self.connection_string = config['azure']['connection_string']
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_name = config['azure']['container_name']

        
    def upload_file(self, file_path, destination):
        try:
            if destination == '':
                destination = file_path
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=destination)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            print("Upload Successful")
        except Exception as e:
            print(f"An error occurred: {e}")

    def download_file(self, source, destination, is_signed_url):
        try:
            if destination == '':
                destination = source
            if os.path.isdir(destination):
                destination = os.path.join(destination, source.split('/')[-1])
            if not is_signed_url:
                blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=source)
                with open(destination, "wb") as download_file:
                    download_file.write(blob_client.download_blob().readall())
                print("Download Successful")
            else:
                elements = dict(x.split('=', 1) for x in self.connection_string.split(';') if x)
                account_name = elements.get('AccountName')
                account_key = elements.get('AccountKey')
                sas_token = generate_blob_sas(
                    account_name=account_name,
                    container_name=self.container_name,
                    blob_name=source,
                    account_key=account_key,
                    permission=BlobSasPermissions(read=True),
                    expiry=datetime.now() + timedelta(hours=1) 
                )
                sas_url = f"https://{account_name}.blob.core.windows.net/{self.container_name}/{source}?{sas_token}"
                get_response = requests.get(sas_url)
                if get_response.status_code == 200:
                    with open(source, 'wb') as file:
                        file.write(get_response.content)
                        print("Download Successful")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def list_files(self):
        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blobs_list = container_client.list_blobs()
            files = [blob.name for blob in blobs_list]
            return files
        except Exception as e:
            print(f"An error occurred: {e}")
