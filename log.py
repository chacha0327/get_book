from loguru import logger

book_log = logger.add("book_selenium/books.log")
error_log = logger.add("book_selenium/error.log")

def log_info(context):
    book_log.info(context)

def log_error(context):
    book_log.error(context)

def log_error_log(context):
    error_log.error(context)

