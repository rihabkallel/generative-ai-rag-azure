#https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python,
import os
import json
import base64
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from dotenv import load_dotenv

class Storage:
    def __init__(self):
        load_dotenv()

        self.azure_service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.azure_search_key = os.getenv("AZURE_SEARCH_KEY")
        self.azure_search_index_name = os.getenv("AZURE_INDEX_NAME")

        self.client = SearchIndexClient(self.azure_service_endpoint, AzureKeyCredential(self.azure_search_key))
        self.search_client = SearchClient(self.azure_service_endpoint, self.azure_search_index_name, AzureKeyCredential(self.azure_search_key))


    def generate_id(url):
        encoded_bytes = base64.urlsafe_b64encode(url.encode("utf-8"))
        encoded_str = encoded_bytes.decode("utf-8").rstrip("=")
        return encoded_str

    def flatten_documents(self, documents):
        flattened_documents = []
        for item in documents:
            for content in item["content"]:
                document = {
                    "id":  self.generate_id(content["pageurl"]), # encode the page url to base64
                    "product": item["product"],
                    "domain": item["domain"],
                    "content": content["text"][0],
                    "pageurl": content["pageurl"]
                }
                flattened_documents.append(document)

    def upload_document_to_index(self, document):
        # Read the document from the JSON file
        with open('test_data.json', 'r') as file:
            documents = json.load(file)
            
        # Upload the document
        # An upload action is similar to an "upsert" where the document will be
        # inserted if it is new and updated/replaced if it exists. All fields are replaced in the update case.
        result = self.search_client.upload_documents(documents=self.flatten_documents(documents))
        print("Upload of new document succeeded: {}".format(result[0].succeeded))
        return result[0].succeeded

    if __name__ == "__main__":
        upload_document_to_index("<<your user query here?>>")