from bcrypt import checkpw
from sqlalchemy.orm import Session
from datetime import datetime as dt, timedelta
import jwt
from app.database import models as m

key = 'secret'
expire_time = timedelta(days=30)

def get_user(db: Session, username: str) -> m.User | None:
    return db.query(m.User).filter(m.User.username == username).first()

def get_user_by_id(db: Session, id: int) -> m.User | None:
    return db.query(m.User).filter(m.User.id == id).first()

def authenticate(db: Session, username: str, password: str) -> m.User | None:
    try:
        user = get_user(db, username)
        if user and checkpw(password.encode(), user.password.encode()):
            return user
    except:
        pass

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
