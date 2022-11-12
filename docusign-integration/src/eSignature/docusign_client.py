import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients, DateSigned

from jwt_helpers import create_api_client

import logging

class DocuSignClient:

    @classmethod
    def worker(cls, args):
        """
        1. Create the envelope request object
        2. Send the envelope
        """

        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)
        api_client = create_api_client(
            base_path=args["base_path"], access_token=args["access_token"])
        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(
            account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls, args):

        # create the envelope definition
        env = EnvelopeDefinition(
            email_subject="Savvly: Please sign these documents"
        )

        docs = list()
        for doc in args["documents"]:

            #logging.info(f"Encoding document: {doc}")
            docx_b64 = base64.b64encode(doc["docx_bytes"]).decode("ascii")

            document = Document(  # create the DocuSign document object
                document_base64=docx_b64,
                name=doc["name"],
                file_extension=doc["file_extension"],  # many different document types are accepted
                document_id=len(docs) + 1  # a label used to reference the doc
            )

            docs.append(document)

        env.documents = docs

        signers = list()

        logging.info(f"Signer list: {args['signers']}")
        for signer in args["signers"]:

            logging.info(f"Signer: {signer}")
            # Create the signer recipient model
            
            # routingOrder (lower means earlier) determines the order of deliveries
            # to the recipients. Parallel routing order is supported by using the
            # same integer as the order for two or more recipients.

            s = Signer(
                email=signer["signer_email"],
                name=signer["signer_name"],
                recipient_id=len(signers) + 1,

                # This is something of a hack to make sure that we can specify
                # the order of signers. It serializes signing in the order given by
                # the signer list. This allows us to put the Savvly signer at the end
                # of the list for final review and signature. The alternative was to
                # add a routing_order to the api and maybe default it to 1 if not given. 
                # This is a little simpler, and should be fine most of the time. It doesn't
                # stop us from adding routing_order to the api later if we want it.
                routing_order=len(signers) + 1
            )
            
            sign_here = SignHere(anchor_string=signer["sign_here_marker"])
            date_signed = DateSigned(anchor_string=signer["sign_date_marker"])
            s.tabs = Tabs(sign_here_tabs=[sign_here], date_signed_tabs=[date_signed])

            signers.append(s)

        copies = list()
        for copy in args["cc"]:
            # create a cc recipient to receive a copy of the documents
            cc = CarbonCopy(
                email=copy["cc_email"],
                name=copy["cc_name"],
                recipient_id=len(signers) + len(copies) + 1,
                routing_order=len(signers) + 1
            )

            copies.append(cc)

        # Create signHere fields (also known as tabs) on the documents,
        # We"re using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings. So the
        # signHere2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs.
        # sign_here1 = SignHere(
        #     anchor_string="CLIENT_SIGN_HERE",
        # )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        # signer1.tabs = Tabs(sign_here_tabs=[sign_here1])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=signers, carbon_copies=copies)
        env.recipients = recipients

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]

        return env
