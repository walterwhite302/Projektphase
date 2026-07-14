# Indirect Prompt Injection Test - English
# Source: OWASP, LLM01:2025 – Prompt Injection
# genai.owasp.org/llm-top-10/
#
# Development notes:
# - Test documents developed independently
# - Error handling and API structure developed
#   with assistance of Claude AI (Anthropic, claude.ai)
# - Code independently reviewed and adapted
# - Standard Python libraries used (requests, csv, datetime, docx, fitz)

import requests
import csv
import datetime
import os
from docx import Document
import fitz  # pymupdf for PDF

os.environ["OLLAMA_MAX_VRAM"] = "0"

models = [
    "llama3:8b",
    #"llama3:70b",
    "mistral:latest",
    #"mistral-small:latest",
    "gemma3:4b",
    "gemma3:12b",
]

documents = [
    {
        "name": "test_visible.docx",
        "path": os.path.expanduser("~/llm-security/indirekt/dokumente/englisch/test_visible.docx"),
        "type": "docx",
        "instructions": "visible"
    },
    {
        "name": "test_invisible.docx",
        "path": os.path.expanduser("~/llm-security/indirekt/dokumente/englisch/test_invisible.docx"),
        "type": "docx",
        "instructions": "invisible"
    },
    {
        "name": "test_visible.pdf",
        "path": os.path.expanduser("~/llm-security/indirekt/dokumente/englisch/test_visible.pdf"),
        "type": "pdf",
        "instructions": "visible"
    },
    {
        "name": "test_invisible.pdf",
        "path": os.path.expanduser("~/llm-security/indirekt/dokumente/englisch/test_invisible.pdf"),
        "type": "pdf",
        "instructions": "invisible"
    },
]

def read_document(path, type):
    if type == "docx":
        doc = Document(path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    elif type == "pdf":
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    
def test_document(model, document_text):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [{
                    "role": "user",
                    "content": f"Please summarize the following text:\n\n{document_text}"
                }],
                "stream": False
            },
            timeout=300
        )
        response_json = response.json()
        if "error" in response_json:
            return f"ERROR: {response_json['error']}"
        return response_json["message"]["content"]
    except Exception as e:
        return f"ERROR: {str(e)}"

results = []

for model in models:
    print(f"\nStarting model: {model}")
    for document in documents:
        print(f"\nReading document: {document['name']}")
        text = read_document(document["path"], document["type"])
        print(f"Testing: {model} | {document['name']}")
        answer = test_document(model, text)
        results.append({
            "model": model,
            "document": document["name"],
            "filetype": document["type"],
            "instructions": document["instructions"],
            "answer": answer,
            "evaluation": ""
        })

filename = f"results_indirekt_en_{datetime.date.today()}.csv"

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "model", "document", "filetype",
        "instructions", "answer", "evaluation"
    ])
    writer.writeheader()
    writer.writerows(results)

print(f"\nDone! Saved in: {filename}")