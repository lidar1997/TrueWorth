import logging

from view import View
from model import Model


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename="logs.txt")
    logger = logging.getLogger(__name__)
    try:
        model = Model()
        view = View(model.run)

    except Exception as e:
        logger.error(f"An error has accord. error info: {e}")
