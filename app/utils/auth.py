from bcrypt import checkpw, hashpw, gensalt
from sqlalchemy.orm import Session
from datetime import datetime as dt
import jwt
from app.core.config import AppConfig
from app.database import models as m

key = AppConfig.api_secret_key
expire_time = AppConfig.api_key_expire_time

def get_user(db: Session, username: str) -> m.User | None:
    return db.query(m.User).filter(m.User.username == username).first()

def get_user_by_id(db: Session, id: int) -> m.User | None:
    return db.query(m.User).filter(m.User.id == id).first()

def register_user(db: Session, username: str, password: str) -> m.User | None:
    if get_user(db, username):
        return None
    user = m.User(username=username, 
                  password=hashpw(password.encode(), gensalt()))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate(db: Session, username: str, password: str) -> m.User | None:
    user = get_user(db, username)
    if user and checkpw(password.encode(), user.password):
        return user

def update_user(db: Session, user: m.User, 
                username: str, first_name: str = None, 
                last_name: str = None, middle_name: str = None,
                email: str = None, gender: m.Gender = None) -> m.User:
    user.username = username or user.username
    user.first_name = first_name or user.first_name
    user.last_name = last_name or user.last_name
    user.middle_name = middle_name or user.middle_name
    user.email = email or user.email
    user.gender = gender if gender is not None else user.gender
    db.commit()
    db.refresh(user)
    return user

def update_password(db: Session, user: m.User, 
                    old_password: str, new_password: str) -> m.User | None:
    user = authenticate(db, user.username, old_password)
    if not user:
        return None
    user.password = hashpw(new_password.encode(), gensalt())
    db.commit()
    db.refresh(user)
    return user

def get_token(db: Session, username: str, password: str) -> str | None:
    user = authenticate(db, username, password)
    if user:
        return gen_token(user.id)

def gen_token(userId: int) -> str:
    now = dt.utcnow()
    return jwt.encode({'userId': userId,
                       'iat': now,
                       'exp': now + expire_time},
                       key,
                       algorithm="HS256")

def verify_token(db: Session, token: str) -> m.User | None:
    try:
        obj = jwt.decode(token, key, algorithms=["HS256"])
        exp = obj['exp']
        user_id = obj['userId']
        if dt.utcnow() < dt.fromtimestamp(exp):
            user = get_user_by_id(db, user_id)
            return user
    except:
        pass
