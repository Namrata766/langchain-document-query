from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.environ.get("AZURE_CONN_STRING")
container_name = os.environ.get(
    "CONTAINER_NAME")  # this is the name of the container created within Azure storage account
blob_name = os.environ.get("BLOB_NAME")  # this is the name of the Azure storage account
directory_path = "Data"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

for root, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)
        blob_name = os.path.relpath(file_path, directory_path)

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

        print(f"Datei {file_path} erfolgreich zu {blob_name} hochgeladen!")
