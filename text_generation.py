from documented_model import main
from logger_conf import logger
from rhyme_finding import prepare_connection_to_db_texts
from time import sleep


def generate_texts_periodically():
    logger.debug("Started text generator")
    collection = prepare_connection_to_db_texts()
    while collection.count_documents({}) < 30:

        logger.debug(f'Texts in base: {collection.count_documents({})}')
        lines = main(4, False)
        record = {"text": lines}
        logger.debug("Putting text into db")
        collection.insert_one(record)
        sleep(60)

if __name__ == '__main__':
    while(True):
        try:
            generate_texts_periodically()
        except Exception as e:
            logger.error(e)