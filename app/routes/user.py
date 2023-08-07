import json
from ast import Dict
from hmac import new

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.connection import SessionLocal, get_db
from app.models.user import create_user, get_user

from ..utils.redis import get_cache, set_cache

user_router = APIRouter()

class UserCreate(BaseModel):
    """
    UserCreate is a class that describes the request body for creating a new user account.
    """
    username: str
    initial_balance: float



@user_router.post("/register")
async def create_user_account(user: UserCreate, db_conn: Session = Depends(get_db)):
    """
    Create a new user account
    """
    if user.initial_balance < 0:
        raise HTTPException(status_code=400, detail="Initial balance cannot be negative")
    try:
        new_user = create_user(db_conn, user.username, user.initial_balance)
        set_cache(user.username, json.dumps(new_user.as_dict()))
        return {"message": "User created successfully", "data": new_user}
    except Exception as error:
        if "(psycopg2.errors.UniqueViolation)" in str(error):
            raise HTTPException(status_code=400, detail="User already exists") from error

        raise HTTPException(status_code=400, detail=str(error)) from error



@user_router.get("/{username}")
@cache(expire=60)
async def get_user_account(username: str, db_conn: Session = Depends(get_db)):
    """
    Get user account details by username
    """
    if user_data := get_cache(username):
        print(f"User from cache: {user_data}")
        return user_data
    return get_user(db_conn, username)
