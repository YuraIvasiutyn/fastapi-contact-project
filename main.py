from fastapi import FastAPI

from app.api import contacts

app = FastAPI()

app.include_router(contacts.router)


app.get("/")
def read_root():
    return {"message": "Hello World"}

