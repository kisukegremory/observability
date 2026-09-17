import logging
import os
import random

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

logger = logging.getLogger(__name__)

@tracer.start_as_current_span("extract")
def extract():
    logger.debug("Extracted some files")


@tracer.start_as_current_span("transform")
def transform():
    logger.debug("Transform operation")
    if random.choice([False, True]):
        return 1 / 0

@tracer.start_as_current_span("load")
def load():
    logger.info("Loading outputs")


@tracer.start_as_current_span("process")
def main():
    try:
        logger.info("Application Start up")
        extract()
        transform()
        load()
        logger.info("End of process")
    except Exception:
        logger.exception("Falha ao executar função principal")



if __name__ == "__main__":
    main()
