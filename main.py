from fastapi import FastAPI

from app.api import contacts, auth_users

app = FastAPI()

app.include_router(contacts.router)
app.include_router(auth_users.router)


app.get("/")


def read_root():
    return {"message": "Hello World"}

