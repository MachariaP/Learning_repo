from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return{ "message": "Hello World"}

@app.get("/hello")
def hello(name: str = "Alan"):
    return { "message": f"Hello {name}. How are you doing"}
