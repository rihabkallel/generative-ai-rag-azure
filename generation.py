import  os
from openai import AzureOpenAI
from dotenv import load_dotenv


class Generation:
    def __init__(self):
        load_dotenv()

        # Azure Open AI setup
        self.azure_openai_deployment = os.getenv("AZURE_OAI_GPT_DEPLOYMENT")
        self.azure_openai_endpoint = os.getenv("AZURE_OAI_GPT_ENDPOINT")
        self.azure_openai_version = os.getenv("AZURE_OAI_VERSION")
        self.azure_openai_key = os.getenv("AZURE_OAI_API_KEY")

        # Azure AI Search setup
        self.azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT") # Add your Azure AI Search endpoint here
        self.azure_search_key = os.getenv("AZURE_SEARCH_KEY") # Add your Azure AI Search admin key here
        self.azure_search_index_name = os.getenv("AZURE_INDEX_NAME") # Add your Azure AI Search index name here
        self.azure_embedding_model = os.getenv("AZURE_OAI_EMBD_DEPLOYMENT")


        self.client = AzureOpenAI(
            api_key=self.azure_openai_key,  
            api_version=self.azure_openai_version,
            azure_endpoint=self.azure_openai_endpoint,
        )

    def generate_response(self, question):
        message_text = [
            {
                "role": "user",
                 "content": question
            }
        ]

        # https://learn.microsoft.com/en-us/azure/ai-services/openai/references/azure-search?tabs=python
        completion = self.client.chat.completions.create(
            messages=message_text,
            model=self.azure_openai_deployment,
            extra_body={
                "data_sources":[
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": self.azure_search_endpoint,
                            "key": self.azure_search_key,
                            "index_name": self.azure_search_index_name,
                            "authentication": {
                                "type": "api_key",
                                "key": self.azure_search_key,
                            },
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": self.azure_embedding_model
                            },
                            "semantic_configuration": "default",
                            "query_type": "vector_semantic_hybrid",
                        }
                    }
                ]
            },
            temperature=0.6,
            top_p=1,
            max_tokens=800,
        )
        result = completion.model_dump_json(indent=2)
        print(result)
        return result


    if __name__ == "__main__":
        generate_response("<<USER_QUERY>>")