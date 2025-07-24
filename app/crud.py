# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:55 2025

@author: sheik
"""

# app/crud.py

from .supabase_client import supabase
from passlib.context import CryptContext
from .schemas import UserCreate, MessageCreate

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username: str):
    res = (
        supabase
        .from_("users")
        .select("*")
        .eq("username", username)
        .single()
        .execute()
    )
    return res.data if not res.error else None

def create_user(user_in):
    hashed = pwd_ctx.hash(user_in.password)
    payload = {
        "username":      user_in.username,
        "password_hash": hashed,
    }
    res = supabase.from_("users").insert(payload).execute()

    if not res.data:
        raise Exception(f"User creation failed (status {res.status_code})")

    # res.data[0] is the new user row
    return res.data[0]


def get_messages_for_user(user_id: int):
    res = (
        supabase
        .from_("messages")
        .select("*")
        .eq("to_id", user_id)
        .execute()
    )
    return res.data

def create_message(from_user_id: int, msg: MessageCreate):
    payload = {
        "from_id": from_user_id,
        "to_id":   msg.to_id,
        "payload": msg.payload,
        "nonce":   msg.nonce,
    }
    res = supabase.from_("messages").insert(payload).execute()

    # check that we got back some data
    if not res.data:
        # you can also inspect res.status_code if you like:
        raise Exception(f"Message insert failed (status {res.status_code})")

    # res.data is a list of inserted rows
    return res.data[0]