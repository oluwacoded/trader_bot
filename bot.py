import asyncio
import os
import json
import websockets

async def running_bot():
    # Railway pulls the token you saved in your variables securely here
    token = os.getenv("OLYMP_TOKEN")
    url = "wss://olymptrade.com/ds/v6"
    
    if not token:
        print("CRITICAL ERROR: OLYMP_TOKEN variable is missing in Railway!")
        return

    print("Connecting to Olymp Trade data servers...")
    
    try:
        async with websockets.connect(url) as ws:
            # 1. Authenticate the bot session using your JWT token
            auth_packet = {
                "action": "auth",
                "token": token
            }
            await ws.send(json.dumps(auth_packet))
            print("Authentication packet sent. Connection established successfully.")

            # 2. Keep the connection alive and listen to the live stream
            async for message in ws:
                data = json.loads(message)
                
                # This will print the live streaming data directly into your Railway logs
                print(f"Live Stream Data: {data}")
                
                # Your trading strategy and trade execution logic will go here
                
    except Exception as e:
        print(f"Connection error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(running_bot())
    except KeyboardInterrupt:
        print("Bot deployment manually terminated.")
