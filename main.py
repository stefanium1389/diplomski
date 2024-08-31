import json
from aws_provider import AWSProvider
from azure_provider import AzureProvider

def display_menu():
    print("\nPlease choose an option:")
    print("1. Upload a file")
    print("2. Download a file")
    print("x  Exit")
    choice = input("Enter your choice (1/2/3): ")
    return choice

def handle_choice(provider):
    while True:
        choice = display_menu()
        if choice == '1':
            file_path = input("Enter the path to the file you want to upload: ")
            destination = input("(Optional )Enter the destination path in the cloud: ")
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
                    destination = input("(Optional) Enter the destination path to save the file: ")
                    provider.download_file(file_name, destination)
                else:
                    print("Invalid number, please try again.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == 'x' or choice == 'X':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    with open('config.json') as config_file:
        config = json.load(config_file)

    if config['provider'] == "AWS":
        provider = AWSProvider(config)
    elif config['provider'] == "Azure":
       provider = AzureProvider(config)
    else:
        print("Invalid provider specified in config.")
        exit(1)

    handle_choice(provider)

