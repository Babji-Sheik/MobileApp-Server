# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:21 2025

@author: sheik
"""

# app/main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import schemas, crud, auth

app = FastAPI()

# CORS — you can keep the wildcard if you’re not using cookies
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
    if crud.get_user_by_username(user.username):
        raise HTTPException(400, "Username already registered")
    return crud.create_user(user)

@app.post("/login", response_model=schemas.Token)
def login(creds: schemas.UserLogin):
    user = auth.authenticate_user(creds.username, creds.password)
    if not user:
        raise HTTPException(401, "Authentication failed")
    token = auth.create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/messages/fetch", response_model=list[schemas.MessageOut])
def fetch_messages(msg: schemas.UserLogin):
    user = auth.authenticate_user(msg.username, msg.password)
    if not user:
        raise HTTPException(401, "Authentication failed")
    return crud.get_messages_for_user(user["id"])

@app.post("/messages/send", response_model=schemas.MessageOut)
def send_message(msg: schemas.MessageCreate):
    user = auth.authenticate_user(msg.username, msg.password)
    if not user:
        raise HTTPException(401, "Authentication failed")
    return crud.create_message(user["id"], msg)
