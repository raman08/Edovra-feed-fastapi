from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Response, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from db import get_database_strategy
from manager import get_user_manager
from models import User, UserCreate, UserDB, UserUpdate, SocketManager
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

cookie_transport = CookieTransport(cookie_max_age=3600, cookie_secure=False)

auth_backend = AuthenticationBackend(name='cookie_auth', transport=cookie_transport, get_strategy=get_database_strategy)

fastapi_users = FastAPIUsers(get_user_manager, [auth_backend], User, UserCreate, UserUpdate, UserDB)

current_active_user = fastapi_users.current_user(active=True)

app = FastAPI(debug=True)

templates = Jinja2Templates(directory='templates')

app.mount("/static", StaticFiles(directory='static'), name='static')

manager = SocketManager()

origins = [
	"http://localhost",
	"http://localhost:3000",
	"http://127.0.0.1:8000",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/api/auth', tags=['auth'])
app.include_router(fastapi_users.get_register_router(), prefix='/api/auth', tags=['auth'])
app.include_router(fastapi_users.get_users_router(), prefix='/api/user', tags=['user'])

@app.get("/", response_class=HTMLResponse)
def get(request: Request):
	return templates.TemplateResponse('home.html', {"request": request})


@app.get("/feed", response_class=HTMLResponse)
def get(request: Request):
	return templates.TemplateResponse('feed.html', {"request": request})


# @app.get("/login", response_class=HTMLResponse)
# def get(request: Request):
# 	return templates.TemplateResponse('home.html', {"request": request})


# @app.get('/api/current_user', tags=['api'])
# async def get_user(request: Request, user: UserDB = Depends(current_active_user)):
# 	return {"user": user}


# @app.get('/api/protected', tags=['api'])
# def protected(user: UserDB = Depends(current_active_user)):
# 	return {"message": f'Welcome Back {user}'}

@app.websocket("/ws/feed")
async def feed(websocket: WebSocket):

	user = websocket.cookies.get('current_user_name')
	print(user)
	if not user:
		user = "Guest"

	await manager.connect(websocket, user)

	response = {"user": user, "message": "Connected Sucessfully"}
	await manager.broadcast(response)

	try:
		while True:
			print("Waiting.....")
			feed = await websocket.receive_json()
			await manager.broadcast(feed)

	except WebSocketDisconnect:
		manager.disconnect(websocket, user)
		response["message"] = "Disconnected"
		await manager.broadcast(response)
