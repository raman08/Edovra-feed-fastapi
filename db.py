import motor.motor_asyncio
from fastapi import Depends
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users_db_mongodb.access_token import MongoDBAccessTokenDatabase
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from models import UserDB, AccessToken, UserCreate

DATABASE_URL = "mongodb+srv://fastAPIadmin:czNF6oyxdJQnNK1r@fastapiuser.fydgv.mongodb.net/fast_api_user_auth?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(
	DATABASE_URL, uuidRepresentation="standard"
)

db = client["fast_api_user_auth"]

user_collection = db["users"]
access_tokens_collection = db["access_tokens"]

async def get_user_db():
	yield MongoDBUserDatabase(UserDB, user_collection)

async def get_access_token_db():
	yield MongoDBAccessTokenDatabase(AccessToken, access_tokens_collection)


def get_database_strategy(
	access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy[UserCreate, UserDB, AccessToken]:
	return DatabaseStrategy(access_token_db, lifetime_seconds=3600)

