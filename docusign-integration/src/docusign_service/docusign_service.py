#!/usr/bin/env python3

import io
import json
import logging
from os import path
import os
import sys
import subprocess
from wsgiref.util import FileWrapper
from flask import Response

import requests
from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException
from jwt_helpers import get_jwt_token, get_private_key
from eSignature.docusign_client import DocuSignClient
from docusign_esign import EnvelopesApi

from config.jwt_config import DS_JWT
from jwt_helpers.jwt_helper import create_api_client

# pip install DocuSign SDK
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'docusign_esign'])

SCOPES = [
    "signature", "impersonation"
]


class DocuSignService:

    def __init__(self):
        self.api_client = ApiClient()
        self.api_client.set_base_path(DS_JWT["authorization_server"])
        self.api_client.set_oauth_host_name(DS_JWT["authorization_server"])

        self.private_key = get_private_key(DS_JWT["private_key_file"]).encode("ascii").decode("utf-8")

        # try:
        #     self.send_document()
        # except ApiException as err:
        #         body = err.body.decode('utf8')

        #         if "consent_required" in body:
        #             consent_url = self.get_consent_url()
        #             print("Open the following URL in your browser to grant consent to the application:")
        #             print(consent_url)
        #             consent_granted = input("Consent granted? Select one of the following: \n 1)Yes \n 2)No \n")
        #             if consent_granted == "1":
        #                 self.send_document()
        #             else: 
        #                 sys.exit("Please grant consent")

    def get_consent_url(self):
        url_scopes = "+".join(SCOPES)

        # Construct consent URL
        redirect_uri = "https://developers.docusign.com/platform/auth/consent"
        consent_url = f"https://{DS_JWT['authorization_server']}/oauth/auth?response_type=code&" \
                      f"scope={url_scopes}&client_id={DS_JWT['ds_client_id']}&redirect_uri={redirect_uri}"

        return consent_url

    def get_token(self):
        # Call request_jwt_user_token method
        token_response = get_jwt_token(self.private_key, SCOPES, DS_JWT["authorization_server"], DS_JWT["ds_client_id"],
                                       DS_JWT["ds_impersonated_user_id"])
        self.access_token = token_response.access_token

        # Save API account ID
        self.user_info = self.api_client.get_user_info(self.access_token)
        self.accounts = self.user_info.get_accounts()
        self.api_account_id = self.accounts[0].account_id
        self.base_path = self.accounts[0].base_uri + "/restapi"

        return {"access_token": self.access_token, "api_account_id": self.api_account_id, "base_path": self.base_path}

    def get_args(self, documents, signers, copies):
        envelope_args = {
            "documents": documents,
            "signers": signers,
            "cc": copies,
            "status": "sent",
        }

        args = {
            "account_id": self.api_account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        #logging.info(f"args: {args}")

        return args

    def send_document(self, request):
        self.get_token()

        req_data = request.get_json()

        signers = req_data["signers"]

        logging.info(f"Got signers from req_data: {signers}")
        
        
        copies = req_data["cc"]

        logging.info(f"Got CC list from req_data: {copies}")

        documents = req_data["documents"]

        documents_resolved = list()
        for document in documents:
            docx_bytes = self.get_document_from_template_service(document["doc_id"], document["document_data"])

            documents_resolved.append({
                "name": document["name"],
                "file_extension": "docx",
                "doc_id": document["doc_id"],
                "docx_bytes": docx_bytes
            })

        args = self.get_args(documents_resolved, signers, copies)
        envelope_id = DocuSignClient.worker(args)
        logging.info("Your envelope has been sent.")
        logging.info(envelope_id)

        return envelope_id, 200

    def get_document_from_template_service(self, doc_id, doc_data):

        logging.info(f"Getting {doc_id} from template service with data: {doc_data}")

        res = requests.post(
            url=f"http://docusign-integration.2f0d5af8eca54c96b6ae.eastus.aksapp.io/documents/template/{doc_id}/render",
            json={
                "document_data": doc_data
            },
            headers={
                "content-type": "application/json"
            }
        )

        return res.content


    """
        doc can be "archive" or "combined". "Archive" will return a zip of
        the documents in the envelope. "combined" will return a single PDF containing
        all documents together. In these modes, doc_id is ignored.

        If doc is not "archive" or "combined" (i.e. any other value), then the 
        doc must contain the document ID of the requested document in the envelope,
        generally starting at "1" for the first document. 
    """
    def retrieve_documents(self, envelope_id, document):

        logging.info(f"Getting envelope {envelope_id} document {document}")

        self.get_token()

        api_client = create_api_client(
            base_path=self.base_path, access_token=self.access_token)
        
        env_client = EnvelopesApi(api_client)

        file_name = env_client.get_document(self.api_account_id, document, envelope_id)

        with open(file_name, "rb") as fh:
            buf = io.BytesIO(fh.read())

        buf.seek(0)

        file_contents = FileWrapper(buf)

        os.remove(file_name)

        mime_type = "application/pdf"

        if document == "archive":
            mime_type = "application/zip"

        return Response(
            file_contents,
            mimetype=mime_type,
            direct_passthrough=True,
        )


    def retrieve_envelope_document_list(self, envelope_id):

        self.get_token()

        api_client = create_api_client(
            base_path=self.base_path, access_token=self.access_token)
        
        env_client = EnvelopesApi(api_client)
        
        docs = env_client.list_documents(self.api_account_id, envelope_id, include_metadata=True)


        docs_rv = [ { 'name': doc.name, 'id': doc.document_id } for doc in docs.envelope_documents ]
        logging.info(f"docs: {docs_rv}")

        return { 'documents': docs_rv }


    def envelope_information(self, envelope_id):

        self.get_token()

        api_client = create_api_client(
            base_path=self.base_path, access_token=self.access_token)
        
        env_client = EnvelopesApi(api_client)
        
        env = env_client.get_envelope(self.api_account_id, envelope_id)
        print(env)


        recips = env_client.list_recipients(self.api_account_id, envelope_id)
        print(recips)

        signers = [ { "name": s.name, "email": s.email, "status": s.status, "signed_date_time": s.signed_date_time } for s in recips.signers]

        return {
            "envelope": {
                "status": env.status,
                "status_changed_date_time": env.status_changed_date_time,
                "sent_date_time": env.sent_date_time,
                "voided_date_time": env.voided_date_time,
                "voided_reason": env.voided_reason,
                "envelope_id": env.envelope_id,
                "envelope_custom_metadata": env.envelope_custom_metadata,
                "completed_date_time": env.completed_date_time,
                "created_date_time": env.created_date_time,
                "expire_date_time": env.expire_date_time,
                "signers": signers 
            }
        }
