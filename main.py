from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from google.cloud import firestore
from google.oauth2 import service_account

app = FastAPI()

# Initialize Firestore
credentials = service_account.Credentials.from_service_account_file("boreal-rain-441609-q9-302220893b4c.json")
db = firestore.Client(credentials=credentials)

# I couldn't find any relaible resource so iused chat gpt for this Initialization of firestore 

# models
class User(BaseModel):
    username: str
    email: str
    project_id: int

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

# CRUD Endpoints
@app.post("/add_users")
def add_user(user: User):
    doc_ref = db.collection("users").document()
    user_data = {
        "username": user.username,
        "email": user.email,
        "project_id": user.project_id
    }
    doc_ref.set(user_data)
    return {"user_id": doc_ref.id, **user_data}

@app.get("/get_users")
def get_users():
    users = [doc.to_dict() | {"user_id": doc.id} for doc in db.collection("users").stream()]
    return users

@app.patch("/update_users/{user_id}")
def update_user(user_id: str, user: UpdateUser):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Error")
    updates = {k: v for k, v in user.dict().items() if v is not None}
    doc_ref.update(updates)
    return {"user_id": user_id, **updates}

@app.delete("/delete_users/{user_id}")
def delete_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Error")
    doc_ref.delete()
    return {"message": f"User {user_id} deleted"}