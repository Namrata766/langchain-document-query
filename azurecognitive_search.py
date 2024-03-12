import os

import openai
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import AzureBlobStorageContainerLoader, PyPDFLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings

load_dotenv()

model: str = "text-embedding-ada-002"

vector_store_address: str = os.environ.get("AZURE_COGNITIVE_SEARCH_SERVICE_URL")

openai.api_type = "azure"
openai.api_key = os.environ.get("AZURE_OPENAI_KEY")
openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-03-15"

embeddings: OpenAIEmbeddings = OpenAIEmbeddings(model=model)

index_name: str = "langchain-vector-demo"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=os.environ.get("AZURE_COGNITIVE_SEARCH_API_KEY"),
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)

pdf_folder_path = "Data"
documents = []
for file in os.listdir(pdf_folder_path):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder_path, file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)
print("chunked doc:", chunked_documents)
vector_store.add_documents(documents=chunked_documents)

loader = AzureBlobStorageContainerLoader(
    conn_str=os.environ.get("AZURE_CONN_STRING"),
    container=os.environ.get("CONTAINER_NAME"),
)
documents = loader.load()
print("from BLOB:", documents)

text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
docs = text_splitter.split_documents(documents)
vector_store.add_documents(documents=docs)

print("Data loaded into vectorstore successfully")