# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:55 2025

@author: sheik
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from .auth import get_password_hash, authenticate_user

# Create a new user
def create_user(db: Session, user: schemas.UserCreate):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Fetch messages for a user
def get_messages_for_user(db: Session, user_id: int):
    return db.query(models.Message).filter(models.Message.to_id == user_id).all()

# Create & store a new message
def create_message(db: Session, from_user_id: int, msg: schemas.MessageCreate):
    db_msg = models.Message(
        from_id=from_user_id,
        to_id=msg.to_id,
        payload=msg.payload,
        nonce=msg.nonce
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg