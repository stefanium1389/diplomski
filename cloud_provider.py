from abc import ABC, abstractmethod

class CloudProvider(ABC):
    
    @abstractmethod
    def upload_file(self, file_path, destination):
        pass

    @abstractmethod
    def download_file(self, source, destination, is_signed_url):
        pass
    
    @abstractmethod
    def list_files(self):
        pass
