# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 01:24:20 2025

@author: sheik
"""

import os
from supabase import create_client, Client

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
