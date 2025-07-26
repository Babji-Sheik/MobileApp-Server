# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:21 2025

@author: sheik
"""

# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import schemas, crud, auth

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate):
    # Check if username already exists
    if crud.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    # Create and return new user
    return crud.create_user(user)

@app.post("/login", response_model=schemas.UserOut)
def login(creds: schemas.UserLogin):
    user = auth.authenticate_user(creds.username, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return user

@app.post("/messages/fetch", response_model=list[schemas.MessageOut])
def fetch_messages(msg: schemas.UserLogin):
    user = auth.authenticate_user(msg.username, msg.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return crud.get_messages_for_user(user["id"])

@app.post("/messages/send", response_model=schemas.MessageOut)
def send_message(msg: schemas.MessageCreate):
    user = auth.authenticate_user(msg.username, msg.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return crud.create_message(user["id"], msg)
@app.get("/users/search/{username}", response_model=schemas.UserOut)
def search_user(username: str):
    user = crud.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user["id"],
        "username": user["username"]
    }
