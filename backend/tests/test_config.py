from backend.core.config import DatabaseConfig



class TestConfig:
    def test_db_config(self):
        DatabaseConfig.get_connection_str()