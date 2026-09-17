import logging
import random
import sys
from time import sleep

import requests

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


def main():

    while True:
        choises = ["health", f"items/{random.randint(1, 1000)}", "topics", "sales", "unexpected" , "not_found"]
        choise = f"http://localhost:8000/{random.choice(choises)}"
        res = requests.get(choise, timeout=2)
        logger.info(f"{choise} - {res.status_code} - {res.json()}")
        sleep(1)


if __name__ == "__main__":
    main()
