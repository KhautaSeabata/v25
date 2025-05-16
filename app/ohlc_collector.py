import asyncio
from datetime import datetime, timezone
from collections import defaultdict
from app.ws_handler import connect_deriv
from app.firebase_client import db

class OHLCCollector:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.current_minute = None
        self.ticks = []

    def _get_minute_epoch(self, epoch):
        # Floor epoch to minute boundary
        return epoch - (epoch % 60)

    async def run(self):
        async for tick in connect_deriv(self.symbol):
            epoch = tick["epoch"]
            quote = tick["quote"]
            minute = self._get_minute_epoch(epoch)

            if self.current_minute is None:
                self.current_minute = minute

            if minute == self.current_minute:
                self.ticks.append(quote)
            else:
                # Minute changed, save OHLC for previous minute
                ohlc = self.calculate_ohlc(self.ticks, self.current_minute)
                await self.save_to_firebase(ohlc)
                # Reset for new minute
                self.current_minute = minute
                self.ticks = [quote]

    def calculate_ohlc(self, prices, minute_epoch):
        o = prices[0]
        h = max(prices)
        l = min(prices)
        c = prices[-1]
        # Convert epoch to ISO string for Firestore document
        dt = datetime.fromtimestamp(minute_epoch, timezone.utc).isoformat()

        return {
            "timestamp": dt,
            "open": o,
            "high": h,
            "low": l,
            "close": c
        }

    async def save_to_firebase(self, ohlc):
        print(f"Saving OHLC: {ohlc}")
        doc_ref = db.collection("vix25_ohlc").document(ohlc["timestamp"])
        doc_ref.set(ohlc)
