# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:57:37 2025

@author: sheik
"""

import datetime
from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at    = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    messages_sent     = relationship("Message", back_populates="sender", foreign_keys="Message.from_id")
    messages_received = relationship("Message", back_populates="recipient", foreign_keys="Message.to_id")
    

class Message(Base):
    __tablename__ = "messages"
    id         = Column(Integer, primary_key=True, index=True)
    from_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    payload    = Column(Text, nullable=False)
    nonce      = Column(Text, nullable=False)
    timestamp  = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    delivered  = Column(Boolean, default=False)
    read       = Column(Boolean, default=False)

    sender    = relationship("User", back_populates="messages_sent", foreign_keys=[from_id])
    recipient = relationship("User", back_populates="messages_received", foreign_keys=[to_id])