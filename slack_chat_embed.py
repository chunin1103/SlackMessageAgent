import pymongo
import requests
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
HF_TOKEN = os.getenv("HF_TOKEN")
# MongoDB client setup
client = pymongo.MongoClient(MONGO_URI)

db = client.SlackChat
collection = db.SlackMessage
user_collection = db.User

items = collection.find().limit(5)

embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:

  response = requests.post(
    embedding_url,
    headers={"Authorization": f"Bearer {HF_TOKEN}"},
    json={"inputs": text})

  if response.status_code != 200:
    raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

  return response.json()

# # Generate Embeddings for all the documents in the collection
# for doc in collection.find({'text':{"$exists": True}}).limit(50):
#   doc['text_embedding_hf'] = generate_embedding(doc['text'])
#   collection.replace_one({'_id': doc['_id']}, doc)


query = "Any recommendation on financial consolitation software?"
print(f"Query: {query}\n")

results = collection.aggregate([
    {"$vectorSearch": 
      {
        "queryVector": generate_embedding(query),
        "path": "text_embedding_hf",
        "numCandidates": 100,
        "limit": 4,
        "index": "ChatEmbeddings",
      }
    },    
    {
        "$lookup": {
            "from": "User",  # Name of the User collection
            "localField": "user_id",  # Field in SlackMessage
            "foreignField": "id",  # Corresponding field in User collection
            "as": "user_details"  # Field name for the joined data
        }
    },
    {
        "$unwind": "$user_details"  # Unwind the user details to make them accessible
    },
    {
        "$project": {
            "username": "$user_details.username",
            "first_name": "$user_details.first_name",
            "last_name": "$user_details.last_name",
            "recommendation": "$text"
        }
    }

]);

# Output results
for document in results:
    print(f'User: {document["username"]} - {document["first_name"]} {document["last_name"]},\nRecommendation: {document["recommendation"]}\n')
