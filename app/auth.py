# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:58:00 2025

@author: sheik
"""

# app/auth.py

from .supabase_client import supabase
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import datetime, timedelta
import os, jwt

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def authenticate_user(username: str, password: str):
    res = (
        supabase
        .from_("users")
        .select("id, username, password_hash")
        .eq("username", username)
        .single()
        .execute()
    )
    if res.error or not res.data:
        return None
    user = res.data
    if not pwd_ctx.verify(password, user["password_hash"]):
        return None
    return {"id": user["id"], "username": user["username"]}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
