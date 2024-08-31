from azure.storage.blob import BlobServiceClient
from cloud_provider import CloudProvider

class AzureProvider(CloudProvider):
    
    def __init__(self, config):
        self.blob_service_client = BlobServiceClient.from_connection_string(config['azure']['connection_string'])
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

    def download_file(self, source, destination):
        try:
            if destination == '':
                destination = source
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=source)
            with open(destination, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
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
