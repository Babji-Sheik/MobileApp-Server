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
    # call via the HTTP API
    res = (
        supabase
        .from_("users")
        .select("id, username, password_hash")
        .eq("username", username)
        .single()
        .execute()
    )

    # if no data came back, user not found
    if not res.data:
        return None

    user = res.data
    # verify the password hash
    if not pwd_ctx.verify(password, user["password_hash"]):
        return None

    # return only the bits your routes need
    return {"id": user["id"], "username": user["username"]}
