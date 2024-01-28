"""
app.py

This one file is all you need to start off with your FastAPI server!
"""

from typing import Optional

from fastapi import FastAPI, status
import requests
# from dotenv import load_env
import os
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn

# load_env()

# Initializing and setting configurations for your FastAPI application is one
# of the first things you should do in your code.
app = FastAPI()

degrees = {}

@app.get("/{degree}")
def get_degree(degree: str):
    try:
        f = open(degree + ".json", 'r')
        s = json.load(f)
        return s
    except (FileNotFoundError):
        return {"Degree not Found": []}

if __name__ == "__main__":
    uvicorn.run("backend_main:app", port=5000, reload=True)
