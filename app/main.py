from fastapi import FastAPI, HTTPException
from redis import Redis
from pydantic import BaseModel
import os
import datetime

app = FastAPI()
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

class Status(BaseModel):
    status: str

@app.get("/status")
def read_status():
    status = redis_client.get("status")
    last_update = redis_client.get("last_update")
    if status is None:
        raise HTTPException(status_code=404, detail="Status not found")
    return {"status": status, "last_update": last_update}

@app.post("/status")
def create_status(status: Status):
    redis_client.set("status", status.status)
    last_update = datetime.datetime.utcnow().isoformat()
    redis_client.set("last_update", last_update)
    return {"message": "Status created", "last_update": last_update}
