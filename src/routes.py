#1.  **Indexing & Searching:** Your program should parse the document `body`, build an index, and accept a query string to find relevant documents.
#2.  **TF-IDF Ranking:** Search results must be ranked and sorted according to their TF-IDF (Term Frequency-Inverse Document Frequency) score.
#3.  **Code Quality & Documentation:** Write clean, readable code. Provide a `README.md` with instructions on how to build and run your project. Be prepared to discuss your development process and design choices.
#4.  **Testing:** Include unit tests that cover the implementation details of your search engine (e.g., indexing, scoring, ranking).

# 1. Retrieve documents from local data source in data/documents.json
from collections import Counter, defaultdict
import json
import math
import uvicorn
import os
import re
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Query

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
    index = defaultdict(dict)
    for doc in documents:
        doc_id = doc["id"]
        text = f"{doc.get('title','')} {doc.get('body','')}"
        counts = Counter(tokenize(text))
        for token, cnt in counts.items():
            index[token][doc_id] = cnt
    return index

index = build_index(document)
N = len(document)  # total number of documents

#==================== Compute IDF =====================

def compute_idf(index, N):
    idf = {}
    for term, postings in index.items():
        df = len(postings)  # number of docs containing this term
        idf[term] = math.log((N + 1) / (df + 1)) + 1  # smoothed IDF
    return idf

idf = compute_idf(index, N)

#fast lookups of documents by id

doc_map = {d["id"]: d for d in document}

#==================== Search & Ranking =====================

#Search function that returns ranked documents based on TF-IDF scores

def score_query_terms(query_terms, index=index, idf=idf):
    scores = defaultdict(float)
    for term in query_terms:
        if term not in index:
            continue #skip terms not in index
        # Compute TF-IDF scores for each document
        for doc_id, tf in index[term].items():
            scores[doc_id] += tf * idf.get(term, 0.0)
    return scores


 #Get ranked documents from scores

def get_ranking_from_scores(scores, doc_map, top_k: Optional[int] = None):
    ranked_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if top_k:
        ranked_docs = ranked_docs[:top_k]
    results = []
    for doc_id, score in ranked_docs:
        doc = doc_map.get(doc_id)
        if not doc:
            continue
        results.append({
            "id": doc.get("id"),
            "title": doc.get("title"),
            "body": doc.get("body"),
            "score": round(score, 4)
            })
    return results

# Wrapper function to handle search queries

def search_query(query: str, index=index, idf=idf, doc_map=doc_map, top_k: Optional[int] = 10):
    query_terms = tokenize(query)
    if not query_terms:
        return {"count": 0, "documents": []}
    scores = score_query_terms(query_terms, index, idf)
    results = get_ranking_from_scores(scores, doc_map, top_k)
    return {"count": len(results), "documents": results}

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

@app.get("/idf")
def get_idf():
    return idf

@app.get("/api/search")
def search_documents(query: str = Query(...), top_k: Optional[int] = None):
    return search_query(query, top_k=top_k)
    
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



    


