import asyncio, websockets

CONNS = set()

async def handler(ws):
    CONNS.add(ws)
    try:
        async for msg in ws:
            for c in CONNS:
                if c != ws: await c.send(msg)
    finally:
        CONNS.remove(ws)

async def main():
    async with websockets.serve(handler, "localhost", 8181):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())