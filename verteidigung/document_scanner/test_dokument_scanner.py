# Document Scanner Defense Test - English
# Source: OWASP, LLM01:2025 – Prompt Injection (Indirect)
# genai.owasp.org/llm-top-10/
#
# Development notes:
# - Test documents from previous indirect prompt injection tests used
# - Error handling and API structure developed
#   with assistance of Claude AI (Anthropic, claude.ai)
# - Code independently reviewed and adapted
# - Standard Python libraries used: requests, csv, datetime, docx, fitz

import requests
import csv
import datetime
import os
from docx import Document
import fitz  # pymupdf for PDF

os.environ["OLLAMA_MAX_VRAM"] = "0"

suspicious_patterns = [
    "[ANWEISUNG:",
    "[INSTRUCTION:",
    "ignoriere",
    "ignore",
    "du bist jetzt",
    "you are now",
    "systemprompt",
    "system prompt",
]

def scan_document(text):
    findings = []
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if pattern.lower() in text_lower:
            findings.append(pattern)
    if findings:
        return "SUSPICIOUS", findings
    return "CLEAN", []

def read_document(path, filetype):
    if filetype == "docx":
        doc = Document(path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    elif filetype == "pdf":
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

documents = [
    {
        "name": "test_sichtbar.docx",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/deutsch/test_sichtbar.docx"),
        "filetype": "docx",
        "language": "DE",
        "instructions": "visible"
    },
    {
        "name": "test_unsichtbar.docx",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/deutsch/test_unsichtbar.docx"),
        "filetype": "docx",
        "language": "DE",
        "instructions": "invisible"
    },
    {
        "name": "test_sichtbar.pdf",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/deutsch/test_sichtbar.pdf"),
        "filetype": "pdf",
        "language": "DE",
        "instructions": "visible"
    },
    {
        "name": "test_unsichtbar.pdf",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/deutsch/test_unsichtbar.pdf"),
        "filetype": "pdf",
        "language": "DE",
        "instructions": "invisible"
    },
    {
        "name": "test_visible.docx",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/englisch/test_visible.docx"),
        "filetype": "docx",
        "language": "EN",
        "instructions": "visible"
    },
    {
        "name": "test_invisible.docx",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/englisch/test_invisible.docx"),
        "filetype": "docx",
        "language": "EN",
        "instructions": "invisible"
    },
    {
        "name": "test_visible.pdf",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/englisch/test_visible.pdf"),
        "filetype": "pdf",
        "language": "EN",
        "instructions": "visible"
    },
    {
        "name": "test_invisible.pdf",
        "path": os.path.expanduser("~/llm-security/angriffe/indirekt/dokumente/englisch/test_invisible.pdf"),
        "filetype": "pdf",
        "language": "EN",
        "instructions": "invisible"
    },
]

results = []

for document in documents:
    print(f"\nScanning: {document['name']}")
    text = read_document(document["path"], document["filetype"])
    scan_result, findings = scan_document(text)

    print(f"Result: {scan_result}")
    if findings:
        print(f"Found patterns: {findings}")

    results.append({
        "document": document["name"],
        "language": document["language"],
        "filetype": document["filetype"],
        "instructions": document["instructions"],
        "scan_result": scan_result,
        "patterns_found": ", ".join(findings),
        "evaluation": ""
    })

filename = f"results_document_scanner_{datetime.date.today()}.csv"

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "document", "language", "filetype",
        "instructions", "scan_result",
        "patterns_found", "evaluation"
    ])
    writer.writeheader()
    writer.writerows(results)

print(f"\nDone! Saved in: {filename}")