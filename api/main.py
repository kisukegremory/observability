import logging
import random

from fastapi import FastAPI
from opentelemetry import metrics, trace

from src import config
from src.errors import unhandled_exception_handler

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
sales_counter = meter.create_counter("sales_created_total")

if config.is_opentelemetry_active():
    logger.info("OpenTelemetry is Active")

app = FastAPI()
app.add_exception_handler(Exception, unhandled_exception_handler)


# Health Check
@app.get("/health")
async def health():
    return {"status": "ok"}


# Dynamic Path
@app.get("/items/{item_id}")
def work(item_id: str):
    return {"item_id": item_id}


# Static Path
@app.get("/topics")
def topics():
    return {"topic_id": random.randint(1, 20)}


# Manual Meter
@app.get("/sales")
def sales():
    with tracer.start_as_current_span("sales_type_select") as span:
        sales_type = random.choice([{"type": "finance"}, {"type": "food"}])
        payment_type = random.choice([{"payment_type": "credit"}, {"payment_type": "money"}])
        span.set_attributes(sales_type)
        span.set_attributes(payment_type)
        sales_counter.add(1, attributes=sales_type)
    return {"status": "ok"}


# Raises
@app.get("/unexpected")
def unexpected():
    if random.choice([False, True]):
        return 1 / 0
    return {"status_code": 200}
