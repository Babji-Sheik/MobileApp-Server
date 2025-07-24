# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:45 2025

@author: sheik
"""

from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    class Config: orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    username: str      # credentials for simple auth
    password: str
    to_id: int
    payload: str
    nonce: str

class MessageOut(BaseModel):
    id: int
    from_id: int
    to_id: int
    payload: str
    nonce: str
    timestamp: datetime
    delivered: bool
    read: bool
    class Config: orm_mode = True