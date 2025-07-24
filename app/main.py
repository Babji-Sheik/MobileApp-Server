# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:21 2025

@author: sheik
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import database, schemas, crud, auth


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ← allow all origins
    allow_credentials=True,       # if you use cookies/auth headers
    allow_methods=["*"],          # allow GET, POST, PUT, DELETE…
    allow_headers=["*"],          # allow any headers
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.UserOut)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return user

@app.post("/messages/fetch", response_model=list[schemas.MessageOut])
def fetch_messages(
    msg: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, msg.username, msg.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return crud.get_messages_for_user(db, user.id)

@app.post("/messages/send", response_model=schemas.MessageOut)
def send_message(
    msg: schemas.MessageCreate,
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, msg.username, msg.password)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return crud.create_message(db, user.id, msg)