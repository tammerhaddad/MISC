import asyncio
import websockets

async def capture_messages():
    url = "wss://territorial.io/s52/"  # WebSocket URL
    print(f"Connecting to {url}...")
    
    try:
        async with websockets.connect(url) as websocket:
            print("Connected. Listening for messages...")
            
            # Send a simple message or a handshake (if required)
            # Try sending a simple "ping" message or the message that the server expects
            await websocket.send("ping")  # Modify this based on the server protocol
            
            while True:
                try:
                    # Receive messages
                    message = await websocket.recv()
                    print("Received:", message)
                    
                    # Optionally, send a response back to the server
                    # await websocket.send("Your message here")
                except websockets.ConnectionClosed as e:
                    print("Connection closed:", e)
                    break
    except Exception as e:
        print("Error:", e)

# Run the WebSocket message capture
asyncio.run(capture_messages())