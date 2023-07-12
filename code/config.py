import os

##################### MongoDB Connections #####################
MONGO_CONNECTION_URI = os.getenv("MONGO_CONNECTION_URI", "mongodb+srv://<username>:<pwd>@retail-demo.2wqno.mongodb.net/?retryWrites=true&w=majority")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "sample")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "vectest")



