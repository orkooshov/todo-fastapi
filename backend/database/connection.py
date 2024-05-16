from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import DatabaseConfig as db_conf
from app.database import models


engine = create_engine(db_conf.get_connection_str(),
                       echo=db_conf.echo,
                       pool_size=db_conf.pool_size)

def initialize_database() -> None:
    create_all_tables()

def create_all_tables() -> None:
    models.Base.metadata.create_all(bind=engine)
