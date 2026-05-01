import json
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = 'https://bpcvatwasmuunonabhuo.supabase.co'

raw_key = os.environ["SUPABASE_KEY"]

# Handle both cases: plain string OR JSON
try:
    parsed = json.loads(raw_key)
    if isinstance(parsed, dict):
        SUPABASE_KEY = parsed.get("SUPABASE_KEY")
    else:
        SUPABASE_KEY = raw_key
except json.JSONDecodeError:
    SUPABASE_KEY = raw_key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)