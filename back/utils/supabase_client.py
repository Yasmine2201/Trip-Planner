from supabase import Client, create_client
from dotenv import load_dotenv
import os

load_dotenv()

class SupabaseClient:
    _instance: Client = None

    __url: str = os.getenv("SUPABASE_URL")
    __key: str = os.getenv("SUPABASE_KEY")

    @staticmethod
    def get():
        if SupabaseClient._instance is None:
            SupabaseClient._instance = create_client(
                SupabaseClient.__url,
                SupabaseClient.__key,
            )
        return SupabaseClient._instance