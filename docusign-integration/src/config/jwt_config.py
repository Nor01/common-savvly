from os import environ


DS_JWT = {
    "ds_client_id": "44b84127-e473-42e9-8c2e-e416c7237e4a",
    "ds_impersonated_user_id": "83ee8bc7-f86e-4c6b-ace1-b74dc9cb3807",  # The id of the user.
    "private_key_file": "../private.key", # Create a new file in your repo source folder named private.key then copy and paste your RSA private key there and save it.
    "authorization_server": "account-d.docusign.com",
    #"doc_docx": "savvly_new_subscription_contract.docx",
    #"doc_pdf": "World_Wide_Corp_lorem.pdf"
}

if "PRIVATE_KEY_FILE" in environ:
    DS_JWT["private_key_file"] = environ.get("PRIVATE_KEY_FILE")


