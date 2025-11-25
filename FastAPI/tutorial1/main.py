from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return { "message": "Hello World!"}

@app.get("/hello")
def hello(name: str = "Alan", age = 24):
    return { "message" : f"My name is {name} and I am {age}years old"}
