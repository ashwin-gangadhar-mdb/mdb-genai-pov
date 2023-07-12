from pymongo import MongoClient
import pandas as pd
from config import MONGO_CONNECTION_URI, MONGO_COLLECTION, MONGO_DATABASE
from sentence_transformers import SentenceTransformer, util
from langchain.docstore.document import Document
import requests
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

import re
def replace_ref(text):
    text = re.sub(r'(\[[0-9]{1,2}\])', '', text)
    return text

def split_n_process_rows(text,state):
    op = []
    for ele in map(lambda x:x.strip(), text.split(".")):
        if ele!="":
            op += [(state, ele.strip() + " "+state)]
    return op

# mongodb connection
client = MongoClient(MONGO_CONNECTION_URI)
db = client[MONGO_DATABASE]
col = db[MONGO_COLLECTION]

df = pd.read_json("data/vectorsearch_poc.wikidata.json")
del df['_id']

df['contents'] = df['contents'].apply(replace_ref)

op = []
for row in df[['contents',"State Name"]].iterrows():
    content = row[1][0]
    state = row[1][1]
    op += split_n_process_rows(content, state)

fdf = pd.DataFrame(op,columns=["state", "line"])

lines = list(fdf.line.values)
states = list(fdf.state.values)
corpus_vector = model.encode(lines)
# print(corpus_vector.shape)
recs = list(map(lambda x:{"d":x[0].tolist(), "doc":x[1], "state":x[2]},zip(corpus_vector, lines, states)))
print(len(recs))
col = client['sample']['vectest']
col.delete_many({})
col.insert_many(recs)



# Load directly from wiki
def query_wikipedia(title, first_paragraph_only=True):
  base_url = "https://en.wikipedia.org"
  url = f"{base_url}/w/api.php?format=json&action=query&prop=extracts&explaintext=1&titles={title}"
  if first_paragraph_only:
    url += "&exintro=1"
  data = requests.get(url).json()
  return {"state": title, "doc": list(data["query"]["pages"].values())[0]["extract"]}
# sources = list(map(lambda x:query_wikipedia(x["_id"]), list(col.aggregate([{"$group":{"_id":"$state"}}]))))

