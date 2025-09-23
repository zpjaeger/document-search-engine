#1.  **Indexing & Searching:** Your program should parse the document `body`, build an index, and accept a query string to find relevant documents.
#2.  **TF-IDF Ranking:** Search results must be ranked and sorted according to their TF-IDF (Term Frequency-Inverse Document Frequency) score.
#3.  **Code Quality & Documentation:** Write clean, readable code. Provide a `README.md` with instructions on how to build and run your project. Be prepared to discuss your development process and design choices.
#4.  **Testing:** Include unit tests that cover the implementation details of your search engine (e.g., indexing, scoring, ranking).

# 1. Retrieve documents from local data source in data/documents.json
from collections import defaultdict
import json
import uvicorn
import os
import re
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException

app = FastAPI()


# ===================== Helper Functions =================

# Load documents from a local JSON file
def load_documents(file_path: str) -> List[Dict]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")
    with open(file_path, 'r') as file:
        documents = json.load(file)
    return documents

 #==================== Load Documents =====================

document = load_documents("data/documents.json")
synonyms = load_documents("constants/synonyms.json")

#==================== Tokenization =====================

def tokenize(text: str):
    tokens = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())
    cleaned = [t[:-2] if t.endswith("'s") else t for t in tokens]
    return cleaned


tokens = [tokenize(document["body"]) for document in document]

#==================== Build Index =====================

def build_index(documents):
    index = defaultdict(lambda:defaultdict(int))
    for doc in documents:
        for token in set(tokenize(doc["body"])):
            index[token][doc["id"]] += 1
    return index

# ===================== API Endpoints =====================
# Example endpoint
@app.get("/hello")
def hello():

    return document

@app.get("/synonyms")
def get_synonyms():
    return synonyms

@app.get("/tokens")
def get_tokens():
    return tokens

@app.get("/index")
def get_index():
    index = build_index(document)
    return index

# Return list of document ids
@app.get("/documents")
def list_documents():
    try:
        ids = [d.get("id") for d in document]
    except Exception:
        ids = []
    return {"count": len(ids), "ids": ids}


# Get a single document by id (iterates through `document` and matches `id`)
@app.get("/documents/{doc_id}")
def get_document_by_id(doc_id: str):
    # naive linear search: iterate through documents and return the one with matching id
    for doc in document:
        # support numeric ids or string ids in the JSON
        try:
            if str(doc.get("id")) == str(doc_id):
                return doc
        except Exception:
            # fallback to direct comparison
            if str(doc.get("id")) == str(doc_id):
                return doc
    raise HTTPException(status_code=404, detail=f"Document with id {doc_id} not found")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



    


