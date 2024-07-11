from database.session import get_db
from fastapi import Depends,HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, User, UserCreate, UserLogin
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils import create_access_token, get_password_hash, verify_password, verify_token

login_router = APIRouter(prefix="")

# for swagger ui to keep the token in the header
@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    async with db as session:
        result = await session.execute(
            select(User).filter(User.username == form_data.username)
        )
        user = result.scalars().first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}


@login_router.get("/")
async def root():
    return {"message": "Hello World "}


@login_router.post("/signup", response_model=Token)
async def signup(user: UserCreate, db=Depends(get_db)):
    async with db as session:
        result = await session.execute(
            select(User).filter(User.username == user.username)
        )
        db_user = result.scalars().first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        access_token = create_access_token(data={"sub": new_user.username})
        return {"access_token": access_token, "token_type": "bearer"}


@login_router.post("/login", response_model=Token)
async def login(user: UserLogin, db=Depends(get_db)):
    async with db as session:
        result = await session.execute(
            select(User).filter(User.username == user.username)
        )
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid username or password")
        access_token = create_access_token(data={"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer"}


@login_router.get("/users/me", dependencies=[Depends(verify_token)])
async def read_users_me(token_data: Token = Depends(verify_token)):
    return {"username": token_data.username}

