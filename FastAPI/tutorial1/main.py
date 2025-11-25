from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_message():
    return{ "Message" : "This is FastAPI"}
