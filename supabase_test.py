import os
from dotenv import load_dotenv
from supabase import create_client, Client
from async_test import *
import asyncio

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# Let's try inserting with just an id first to see what happens
async def mainFunction():
    try:
        results = await main_ultra_fast()
        
        # If you want just the text from all candidates flattened:
        print("\n--- All text content ---")
        all_texts = []
        for result in results:
            for candidate in result.candidates:
                for part in candidate.content.parts:
                    all_texts.append(part.text)
                    print(part.text)
                    print(type(part.text))
        # Store in database (example)

        response = (
            supabase.table("responses")
            .insert({"id": 11, "content": all_texts})
            .execute()
        )
        print(f"Stored result in database")

        storedInfo = (
            supabase.table("responses")
            .select("*")
            .execute()
        )

        print(storedInfo)
        
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(mainFunction())

#important note:
#1) if you want to do the insert without any auth, then you have to disable the RLS (row level security).
#2) if you want to insert something into the database, then the columns and the table already has to exist (if your using the above code).