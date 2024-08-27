#!/usr/bin/env python

from fastapi import FastAPI
from chain import youtube_summary_chain
from langserve import add_routes

from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI(
  title="Youtube summary",
  version="1.0",
  description="A simple youtube summarize service",
)

add_routes(
    app,
    youtube_summary_chain,
    path="/youtube-summary",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=int(os.environ["SERVICE_PORT"]))