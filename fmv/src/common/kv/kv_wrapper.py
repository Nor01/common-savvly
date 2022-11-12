import os

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient, KeyVaultSecret
from msrestazure.azure_active_directory import MSIAuthentication

from common.util.config_wrapper import get_config_string_param
from common.util.logging_helper import get_logger
from common.util.timestamp_helper import *

from datetime import datetime
import pytz

utc=pytz.UTC

# -------------------------------------------------------------
# Class AzureKeyVaultWrapper
# -------------------------------------------------------------
class AzureKeyVaultWrapper:
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if AzureKeyVaultWrapper.__instance is None:
            AzureKeyVaultWrapper()
        return AzureKeyVaultWrapper.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
        if AzureKeyVaultWrapper.__instance != None:
            raise Exception("This class is a singleton!")
            return
        AzureKeyVaultWrapper.__instance = self
        self.glogger = get_logger("AzureKeyVaultWrapper")
        self.credentials = None
        self.resource = "https://vault.azure.net/"
        self.kv_name = get_config_string_param('keyVault')
        self.subscription_id = get_config_string_param('kv_subscriptionId')
        """This tries to get a token using MSI, or fallback to SP env variables.
        """
        if "MSI_ENDPOINT" in os.environ:
            self.glogger.debug("MSI_ENDPOINT defined as an Env Var. Getting the credentials from: %s", self.kv_name)
            self.credentials = MSIAuthentication(resource=self.kv_name)
        else:  ### this is from the main direcotry ...
            # self.glogger.debug("Getting the credentials from: %s", self.resource)
            # self.credentials =  ServicePrincipalCredentials(
            self.subscription_id = get_config_string_param('kv_subscriptionId')
            self.tenant_id = get_config_string_param('kv_tenantId')
            self.client_id = get_config_string_param('kv_clientId')
            self.client_secret = get_config_string_param('kv_clientSecret')
            self.credentials = ClientSecretCredential(
                client_id=self.client_id,
                client_secret=self.client_secret,
                tenant_id=self.tenant_id,
                resource=self.resource
            )

        if not self.credentials:
            self.glogger.error("Failed to get credentials from the KV")
        self.key_vault_client = SecretClient(self.kv_name, self.credentials)

    # -----------------------------------------------
    # get the KV Client
    # -----------------------------------------------
    def _get_kv_client(self):
        return self.key_vault_client

    # -----------------------------------------------
    # get the KV Credentials
    # -----------------------------------------------
    def _get_credentials(self):
        return self.credentials

    # -----------------------------------------------
    # get the specified Secret
    # -----------------------------------------------
    def get_secret(self, key: str):
        sec: KeyVaultSecret = self.key_vault_client.get_secret(
            # self.kv_name,  # Your KeyVault URL
            key
            # ""
        )
        expiration: datetime = sec.properties.expires_on
        if expiration:
            expiration = expiration.replace(tzinfo=utc)
            current_time = datetime.utcnow()
            current_time = utc.localize(current_time)

            if expiration < current_time:
                return None
            else:
                return sec.value
        else:
            return sec.value

    # -----------------------------------------------
    # Add Secret to the KV
    # -----------------------------------------------
    def add_secret(self, key: str, value: str):
        self.glogger.debug("Adding secret to keyvault - key=%s", key)
        self.key_vault_client.set_secret(key, value)

    # -----------------------------------------------
    # Add expirable Secret to the KV
    # -----------------------------------------------
    def add_expireable_secret(self, key: str, value: str, expire_hr: int):
        self.glogger.debug("Adding secret to keyvault - key=%s timeout=%s", key, expire_hr)
        exp = get_n_hrs_ago(-expire_hr)
        epoch = datetime.utcfromtimestamp(int(exp))  # start of epoch time
        self.key_vault_client.set_secret(key, value, expires_on=epoch)

    # -----------------------------------------------
    # Does the key exist?
    # -----------------------------------------------
    def key_exists(self, key: str) -> bool:
        secrets = self.key_vault_client.list_properties_of_secrets()
        for secret in secrets:
            # self.glogger.debug("Checking if secret matches secretname=%s, key=%s", secret.name, key)
            if key == secret.name:
                self.glogger.debug("Secret exists in the kv key=%s", key)
                return True
        self.glogger.error("Secret does not exist in the kv key=%s", key)
        return False

    # -----------------------------------------------
    # Delete Secret
    # -----------------------------------------------
    def delete_secret(self, key: str):
        if self.key_exists(key):
            self.glogger.info("Deleting secret from the kv key=%s", key)
            deleted_secret_poller = self.key_vault_client.begin_delete_secret(key)
            deleted_secret_poller.wait()  # Block until the deletion completed
            try:
                self.key_vault_client.purge_deleted_secret(key)
            except Exception as err:
                self.glogger.error("Failed to delete/purge secret key %s from the keyvault. err=%s", key, err)
            return True
        else:
            self.glogger.info("No secret found in the KV for this key to be deleted:%s", key)
            return False

    # -----------------------------------------------
    # Recover Secret kv = AzureKeyVaultWrapper.get_instance()
    # -----------------------------------------------
    def recover_secret(self, key: str):
        self.glogger.info("Recovering secret in the kv key=%s", key)
        recover_secret_poller  = self.key_vault_client.begin_recover_deleted_secret(key)
        recovered_secret = recover_secret_poller.result()
        self.glogger.info("Recovered key=%s name=%s", recovered_secret.id, recovered_secret.name)
        recover_secret_poller.wait()

    # -----------------------------------------------
    # Recover or add
    # -----------------------------------------------
    def _recover_or_add_key(self, key: str, value: str):
        if self.key_exists(key):
            return True
        self.recover_secret(key)
        if self.key_exists(key):
            return True
        self.add_secret(key, value)

    # -----------------------------------------------
    # Add the essential keys to the kv
    # -----------------------------------------------
    def _initialize_mandatory_keys(self):
        self._recover_or_add_key("cosmos-contact-point", "savvly-cosmos-dev-eastus.cassandra.cosmos.azure.com")
        self._recover_or_add_key("cosmos-keyspace", "dev")
        self._recover_or_add_key("cosmos-password", "x9HlT1ob8VFkV77HogU8JyibbZp64ApHCzTjnzOBSJ7B5wHjzmyrf0JKJdOZekhxfB6q7SrarhY7STHee4VDCg==")
        self._recover_or_add_key("cosmos-port", "10350")
        self._recover_or_add_key("cosmos-username", "savvly-cosmos-dev-eastus")

    # -----------------------------------------------
    # Get all the secrets in a dictionary
    # -----------------------------------------------
    def get_all_secrets(self) -> dict:
        secrets = self.key_vault_client.list_properties_of_secrets()
        if not secrets:
            self.glogger.info("Failed to get the secret list from the KV")
            return None
        secret_list = {}
        for secret in secrets:
            rec = self.get_secret(secret.name)
            #self.glogger.info("Secret=%s Secret value=%s", secret.name, rec)
            secret_list[secret.name] = rec
        return secret_list

    # -----------------------------------------------
    # Delete all the secrets
    # -----------------------------------------------
    def delete_all_secrets(self):
        secrets = self.key_vault_client.list_properties_of_secrets()
        for secret in secrets:
            self.delete_secret(secret.name)
            self.glogger.info("Deleted Secret=%s", secret.name)
        self._initialize_mandatory_keys()
        return secrets

    # -----------------------------------------------
    # Get a parameter as a string
    # -----------------------------------------------
    def get_string_param(self, name: str, default: str = "") -> str:
        if self.key_exists(name):
            return self.get_secret(name)
        else:
            return default

    # -----------------------------------------------
    # Get a parameter as an integer
    # -----------------------------------------------
    def get_int_param(self, name: str, default: int = "") -> int:
        if self.key_exists(name):
            return int(self.get_secret(name))
        else:
            return int(default)