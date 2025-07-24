# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:58:00 2025

@author: sheik
"""

# app/auth.py

# app/auth.py

from .supabase_client import supabase
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username: str, password: str):
    res = (
        supabase
        .from_("users")
        .select("id, username, password_hash")
        .eq("username", username)
        .maybe_single()
        .execute()
    )
    user = res.data
    if not user or not pwd_ctx.verify(password, user["password_hash"]):
        return None
    return {"id": user["id"], "username": user["username"], "created_at": user.get("created_at")}