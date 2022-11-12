from common.util.config_wrapper import ReadConfig

if __name__ == '__main__':
    c = ReadConfig.get_instance()

    # print(c.get_debug_level())

    print(c.get_string_value("keyVault"))

    print(c.is_param_local("foo"))
