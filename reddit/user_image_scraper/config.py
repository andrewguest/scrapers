import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass()
class Config:
    reddit_client_id = os.getenv("REDDIT_ID")
    reddit_client_secret = os.getenv("REDDIT_SECRET")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
    reddit_username = os.getenv("REDDITOR")
