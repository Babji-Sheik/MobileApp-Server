# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:58:00 2025

@author: sheik
"""

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import User
from .database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password against its hash
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Authenticate user by username/password
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user