import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import set_default_openai_client

load_dotenv()

client = AsyncOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
)

set_default_openai_client(client)
