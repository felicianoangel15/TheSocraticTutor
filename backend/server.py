from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# ❌ DELETE/COMMENT OUT: from google import adk
#
# ➡️ You need to add the correct import here. ⬅️
#
# If 'adk' is a global variable initialized in a config file (e.g., config.py):
# from .config import adk
#
# OR if it's part of your agent setup:
# from backend.agent_client_setup import adk # Example

from backend.agent import root_agent   # import your agent.py setup

app = FastAPI()

# Allow frontend (React at localhost:5173) to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    message: str

