import json
from aws_provider import AWSProvider
from azure_provider import AzureProvider

def display_menu():
    print("\nPlease choose an option:")
    print("1. Upload a file")
    print("2. Download a file")
    print("x  Exit")
    choice = input("Enter your choice (1/2/x): ")
    return choice

def handle_choice(provider):
    while True:
        choice = display_menu()
        if choice == '1':
            file_path = input("Enter the path to the file you want to upload: ")
            destination = input("(Optional) Enter the destination path in the cloud: ")
            provider.upload_file(file_path, destination)
        elif choice == '2':
            print("Listing all files...")
            files = provider.list_files()
            if not files:
                print("No files found.")
                continue
            
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")

            file_choice = input("Enter the number of the file you want to download: ")
            try:
                file_choice = int(file_choice)
                if 1 <= file_choice <= len(files):
                    file_name = files[file_choice - 1]
                    signed_url_choice = input("(Optional) Use presigned urls? (Y/N): ")
                    is_signed_url = False
                    if signed_url_choice.lower() == "y":
                        is_signed_url = True
                    destination = ''
                    if not is_signed_url:
                        destination = input("(Optional) Enter the destination path to save the file: ")
                    
                    provider.download_file(file_name, destination, is_signed_url)
                else:
                    print("Invalid number, please try again.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == 'x' or choice == 'X':
            print("Exiting the application.")
            exit(0)
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    with open('config.json') as config_file:
        config = json.load(config_file)
        config_keys = list(config.keys())
        for i, key in enumerate(config_keys, 1):
                print(f"{i}. {key}") 
        print("x  Exit")
        while True:  
            provider_choice = input("Enter the number of the provider you want to use: ")
            if provider_choice.lower() == "x":
                print("Exiting the application.")
                exit(0)
            try:
                provider_choice = int(provider_choice)
                if 1 <= provider_choice <= len(config_keys):
                    provider_name = config_keys[provider_choice - 1]
                    if config[provider_name]["provider"] == "AWS":
                        provider = AWSProvider(config[provider_name])
                    elif config[provider_name]["provider"] == "Azure":
                        provider = AzureProvider(config[provider_name])
                    else:
                        print("Invalid provider configuration!")
                        exit(1)
                    handle_choice(provider)
                else:
                    print("Invalid choice, please try again.")

            except ValueError:
                print("Please enter a valid number.")

    # handle_choice(provider)

