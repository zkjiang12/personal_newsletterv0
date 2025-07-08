import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# First, let's just test the connection
try:
    # This will list your tables (if you have any)
    response = supabase.table("planets").select("*").limit(1).execute()
    print("Connection successful!")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
    print("The 'planets' table probably doesn't exist. Check your Supabase dashboard.")

#note need to create the table planets first