from loguru import logger

logger.add("book_selenium/books.log")


def log_info(context):
    logger.info(context)

def log_error(context):
    logger.error(context)


