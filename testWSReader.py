import asyncio
import sys
import websockets

async def capture_messages():
    url = "wss://territorial.io/s52/"  # WebSocket URL
    print(f"Connecting to {url}...")

    try:
        async with websockets.connect(url) as websocket:
            print("Connected. Listening for messages...")

            # The send sits inside the same try as the recv loop. Left outside,
            # a server that closes on the handshake surfaced as "Error:" via the
            # catch-all below instead of "Connection closed:".
            try:
                # Send a simple message or a handshake (if required)
                # Try sending a simple "ping" message or the message that the server expects
                await websocket.send("ping")  # Modify this based on the server protocol

                while True:
                    # Receive messages
                    message = await websocket.recv()
                    print("Received:", message)

                    # Optionally, send a response back to the server
                    # await websocket.send("Your message here")
            except websockets.ConnectionClosed as e:
                print("Connection closed:", e)
    except Exception as e:
        print("Error:", e)
        return 1
    return 0

# Run the WebSocket message capture. Exit non-zero on failure -- every outcome
# used to report success, including a refused connection.
sys.exit(asyncio.run(capture_messages()))
