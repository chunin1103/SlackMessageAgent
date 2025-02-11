import pymongo

client = pymongo.MongoClient(
    "mongodb://chunin1103:hIpMGD2oHY21oAVj@cluster0-shard-00-00.u9nen.mongodb.net:27017,"
    "cluster0-shard-00-01.u9nen.mongodb.net:27017,"
    "cluster0-shard-00-02.u9nen.mongodb.net:27017/"
    "?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
)

db = client.SlackChat
collection = db.SlackMessage

items = collection.find().limit(5)
for item in items:
    print(item)