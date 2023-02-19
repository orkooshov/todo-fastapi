from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database.connection import initialize_database, engine
from app.database.models import User, Task, Subtask


initialize_database()
with Session(engine) as dbsession:
    user = User(username='testa', password='test')
    dbsession.add(user)
    task = Task(title='hello', user=user)
    dbsession.add(task)
    st = Subtask(title='test_subtask', task=task)
    dbsession.add(st)
    dbsession.commit()
