from death_checker.util.check_log import get_logger

# Ready to get Singleton
class Dbhandles():
    __instance = None

    ## ---------------------------------------------
    ## Return the singletone object
    ## ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if Dbhandles.__instance is None:
            Dbhandles()
        return Dbhandles.__instance

    

