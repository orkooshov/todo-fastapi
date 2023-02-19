from app.database.connection import initialize_database
from app.database.tables.Base import Base


def test_connection_ok():
    Base.metadata.tables

def test_initialize_database():
    initialize_database()