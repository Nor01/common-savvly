from kv.kv_wrapper import AzureKeyVaultWrapper

if __name__ == '__main__':
    kv = AzureKeyVaultWrapper.get_instance()

    kv.add_secret("key1", "value10")

    print(kv.get_secret("key1"))
