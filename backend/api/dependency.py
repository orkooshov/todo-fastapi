from backend.database.connection import engine
from sqlalchemy.orm import Session
from fastapi import Header, Depends
from fastapi.exceptions import HTTPException
from backend.database import models as m
from backend.services import auth


async def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

async def authorize(authorization: str | None = Header(None),
                    db: Session = Depends(get_db)) -> m.User:
    if not authorization:
        raise HTTPException(400, 'The authorization header required')
    try:
        token = authorization.split(' ')[1]
    except:
        raise HTTPException(400, 'The authorization header incorrect')
    user = auth.verify_token(db, token)
    if not user:
        raise HTTPException(401, f'Invalid token')
    return user