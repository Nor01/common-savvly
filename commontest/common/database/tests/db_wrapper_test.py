from common.database.db_wrapper import CosmosFactory
import os


if __name__ == '__main__':

    db = CosmosFactory.instance()

    db.get_session()
