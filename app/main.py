from fastapi import FastAPI
import asyncio
from app.ohlc_collector import OHLCCollector

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    collector = OHLCCollector("R_25")
    asyncio.create_task(collector.run())

@app.get("/")
def read_root():
    return {"message": "OHLC collector running"}
