#1.  **Indexing & Searching:** Your program should parse the document `body`, build an index, and accept a query string to find relevant documents.
#2.  **TF-IDF Ranking:** Search results must be ranked and sorted according to their TF-IDF (Term Frequency-Inverse Document Frequency) score.
#3.  **Code Quality & Documentation:** Write clean, readable code. Provide a `README.md` with instructions on how to build and run your project. Be prepared to discuss your development process and design choices.
#4.  **Testing:** Include unit tests that cover the implementation details of your search engine (e.g., indexing, scoring, ranking).

# 1. Retrieve documents from local data source in data/documents.json
import json
import uvicorn
import os
from typing import List, Dict
from fastapi import FastAPI

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

# ===================== API Endpoints =====================
# Example endpoint
@app.get("/hello")
def hello():
    return document

@app.get("/synonyms")
def get_synonyms():
    return synonyms



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



    


