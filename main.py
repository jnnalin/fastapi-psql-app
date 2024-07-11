from database.session import get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, User, UserCreate, UserLogin
from routes import product_router, database_router, login_router
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils import create_access_token, get_password_hash, verify_password, verify_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# for swagger ui to keep the token in the header
app.include_router(login_router)

app.include_router(product_router)


app.include_router(database_router)
