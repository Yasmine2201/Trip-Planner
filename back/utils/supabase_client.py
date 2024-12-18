from __future__ import annotations

from supabase import Client, create_client
from dotenv import load_dotenv
import os

from utils import Singleton

load_dotenv()
URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_KEY")


class SupabaseClient(metaclass=Singleton):

    def __init__(self):
        self.__url: str = URL
        self.__key: str = SUPABASE_SERVICE_KEY
        self.__client: Client = create_client(self.__url, self.__key)

    @property
    def client(self) -> Client:
        return self.__client

    @staticmethod
    def get() -> Client:
        return SupabaseClient().client
