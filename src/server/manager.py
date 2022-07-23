import json
import random
import uuid

from fastapi import WebSocket


class ConnectionManager:
    """It handles ALL players websockets"""

    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def add(self, websocket: WebSocket):
        """Accepts a new Player's websocket and adds it to the list."""
        self.active_connections.add(websocket)

    async def drop(self, websocket: WebSocket):
        """Handles proper disconnect of a Player and removes websocket from the list."""
        self.active_connections.remove(websocket)

    async def update(self, websocket: WebSocket):
        """Receives JSON payload from a websocket and updates client's unique_id if required."""
        payload = await websocket.recv()
        payload = json.loads(payload)

        if not payload["unique_id"]:
            # Generate client's unique ID
            payload["unique_id"] = uuid.uuid4().hex

        if not payload["nickname"]:
            # Check if a nickname was given
            payload["nickname"] = f"Guest{random.randint(10000, 20000)}"

        return payload

    def connections(self):
        """Return a list of all currently active connections."""
        return self.active_connections
