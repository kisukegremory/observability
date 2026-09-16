import logging
import random
import sys

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


def extract():
    logger.debug("Extracted some files")


def transform():
    logger.debug("Transform operation")
    if random.choice([False, True]):
        return 1 / 0

def load():
    logger.debug("Loading outputs")


def main():
    extract()
    transform()
    load()

if __name__ == "__main__":
    logger.info("Application Start up")
    main()
    logger.info("End of process")
