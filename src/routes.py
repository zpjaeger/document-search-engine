#1.  **Indexing & Searching:** Your program should parse the document `body`, build an index, and accept a query string to find relevant documents.
#2.  **TF-IDF Ranking:** Search results must be ranked and sorted according to their TF-IDF (Term Frequency-Inverse Document Frequency) score.
#3.  **Code Quality & Documentation:** Write clean, readable code. Provide a `README.md` with instructions on how to build and run your project. Be prepared to discuss your development process and design choices.
#4.  **Testing:** Include unit tests that cover the implementation details of your search engine (e.g., indexing, scoring, ranking).

# 1. Retrieve documents from local data source in data/documents.json
import json
import uvicorn
import os
from fastapi import FastAPI

app = FastAPI()

# Add logic here
@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    


