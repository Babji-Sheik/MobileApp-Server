# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 01:24:20 2025

@author: sheik
"""

# app/supabase_client.py

from dotenv import load_dotenv

# 1) Load any vars defined in .env into the environment
load_dotenv()

import os
from supabase import create_client, Client

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

# 2) Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
