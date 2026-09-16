import logging
import random
import sys

from opentelemetry import metrics, trace

meter = metrics.get_meter(__name__)
tracer = trace.get_tracer(__name__)
pipe_counter = meter.create_counter("pipeline_counter")

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)

@tracer.start_as_current_span("extract")
def extract():
    logger.info("Extracted some files")

@tracer.start_as_current_span("transform")
def transform():
    logger.info("Transform operation")
    if random.choice([False, True]):
        pipe_counter.add(1, attributes={"success": False})
        return 1 / 0
    pipe_counter.add(1, attributes={"success": True})

@tracer.start_as_current_span("load")
def load():
    span = trace.get_current_span()
    span.set_attributes({"loaded_files":random.randint(1,15)})
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
