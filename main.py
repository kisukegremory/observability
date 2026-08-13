from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def main():
    return {"Nina":"Nyaaaa"}
