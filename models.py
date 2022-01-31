from fastapi_users import models
from fastapi_users.authentication.strategy.db import BaseAccessToken
from fastapi import WebSocket
from typing import List

class User(models.BaseUser):
	name:str

class UserCreate(models.BaseUserCreate):
	name:str

class UserUpdate(models.BaseUserUpdate):
	name:str

class UserDB(User, models.BaseUserDB):
	name:str

class AccessToken(BaseAccessToken):
	pass

class SocketManager:
	def __init__(self) -> None:
		self.active_connections: List[(WebSocket, str)] = []

	async def connect(self, websocket: WebSocket, user: str):
		await websocket.accept()
		self.active_connections.append((websocket, user))

	def disconnect(self, websocket: WebSocket, user: str):
		self.active_connections.remove((websocket, user))

	async def broadcast(self, data:dict):
		for connection in self.active_connections:
			await connection[0].send_json(data)