import sys
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def extract_text_from_email(api_key, endpoint, email_subject):
    credential = AzureKeyCredential(api_key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    documents = [email_subject]

    # Recognize entities in the document
    result = client.recognize_entities(documents=documents)[0]

    for entity in result.entities:
        # Check if the entity is categorized as a phone number
        if entity.category == "PhoneNumber":
            entity.category = "AirwayBillNumber"

        print(f"Entity: {entity.text}, Type: {entity.category}")
        #print(entity)

if __name__ == "__main__":
    # Replace these with your actual API key and endpoint
    azure_text_analytics_api_key = "4c2a75a405e04b439d1e39fb65bce11c"
    azure_text_analytics_endpoint = "https://lang-dev-we-cbit-01.cognitiveservices.azure.com/"

    email_subject = sys.argv[1]

    extract_text_from_email(
        api_key=azure_text_analytics_api_key,
        endpoint=azure_text_analytics_endpoint,
        email_subject=email_subject
    )
