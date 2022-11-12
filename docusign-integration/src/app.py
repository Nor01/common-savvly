#!/usr/bin/env python3

from flask import Flask, request, jsonify

from docusign_service.docusign_service import DocuSignService

import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    level=LOGLEVEL,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)

ds_service = DocuSignService()

@app.post("/signup/senddoc")
def send_doc():
    if request.is_json:
        return ds_service.send_document(request)
    return {"error": "Request must be JSON"}, 415


""" 
    document can be a specific document number from the envelope, 
    or can be 'combined' or 'archive'. 'combined' will return a combined pdf,
    'archive' will return a zip with all documents, and a doc number will return
    the specific document contents.
"""
@app.get("/docusign/<envelope_id>/retrieve/<document>")
def get_envelope_documents(envelope_id, document): 
    return ds_service.retrieve_documents(envelope_id, document)

@app.get("/docusign/<envelope_id>/list")
def get_envelope_doc_list(envelope_id):
    return ds_service.retrieve_envelope_document_list(envelope_id)

@app.get("/docusign/<envelope_id>/info")
def get_envelope_info(envelope_id):
    return ds_service.envelope_information(envelope_id)