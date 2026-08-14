from fastapi import FastAPI
from opentelemetry import trace
import time
import random
from uuid import uuid4

app = FastAPI()
tracer = trace.get_tracer(__name__)


@app.get("/health")
def main():
    with tracer.start_as_current_span("processamento_leve"):
        return {"Nina":"Nyaaaa"}

@tracer.start_as_current_span("calculo_coxinhas")
def calcula_coxinhas():
    span = trace.get_current_span()
    span.set_attribute("user.id",str(uuid4()))


@app.get("/work")
def work():
    with tracer.start_as_current_span("processamento_brabo") as span:
        time_choosed = random.randint(1,5)
        if time_choosed < 3:
            time.sleep(time_choosed)
            calcula_coxinhas()
            span.set_attribute("nina.estado","trabalhando")
            return {"Nina":"Cansadinina!"}
        span.set_attribute("nina.estado","faz_nada")
        return {"Nina":"Me da petisco!"}
