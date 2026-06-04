import asyncio
import os
import json
import websockets

async def running_bot():
    token = os.getenv("OLYMP_TOKEN")
    url = "wss://olymptrade.com/ds/v6"
    
    if not token:
        print("CRITICAL ERROR: OLYMP_TOKEN variable is missing in Railway!")
        return

    print("Connecting to Olymp Trade data servers...")
    
    # Custom headers to mask the cloud server and bypass the 403 Handshake block
    custom_headers = {
        "Origin": "https://olymptrade.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        # Pass the headers directly into the connection request
        async with websockets.connect(url, extra_headers=custom_headers) as ws:
            print("Handshake approved! Sending authentication token...")
            
            # Authenticate the bot session using your JWT token
            auth_packet = {
                "action": "auth",
                "token": token
            }
            await ws.send(json.dumps(auth_packet))
            print("Authentication packet sent. Connection fully active.")

            # Keep the connection alive and listen to the live stream
            async for message in ws:
                data = json.loads(message)
                print(f"Live Stream Data: {data}")
                
    except Exception as e:
        print(f"Connection error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(running_bot())
    except KeyboardInterrupt:
        print("Bot deployment manually terminated.")
