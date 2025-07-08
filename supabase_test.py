import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# Let's try inserting with just an id first to see what happens
try:
    response = (
        supabase.table("responses")
        .update({"id": 3,"name":"supp boi"})
        .execute()
    )
    print("\nSuccessfully inserted with just id:")
    print(response.data)
    
except Exception as e:
    print(f"Error inserting: {e}")

#important note:
#1) if you want to do the insert without any auth, then you have to disable the RLS (row level security).
#2) if you want to insert something into the database, then the columns and the table already has to exist (if your using the above code).