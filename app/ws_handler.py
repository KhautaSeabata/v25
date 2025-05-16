import websockets
import json

async def connect_deriv(symbol: str):
    url = "wss://ws.derivws.com/websockets/v3"
    async with websockets.connect(url) as ws:
        sub_request = {
            "ticks": symbol,
            "subscribe": 1
        }
        await ws.send(json.dumps(sub_request))

        while True:
            response = await ws.recv()
            data = json.loads(response)
            if "tick" in data:
                yield {
                    "epoch": data["tick"]["epoch"],
                    "quote": data["tick"]["quote"]
                }
