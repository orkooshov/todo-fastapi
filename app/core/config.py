from datetime import timedelta
from functools import lru_cache
from os import environ
from dotenv import load_dotenv


load_dotenv()

class DatabaseConfig:
    dialect = 'postgresql'
    driver = 'psycopg2'
    user = environ['DB_USER']
    password = environ['DB_PASS']
    host = environ['DB_HOST']
    port = environ.get('DB_PORT', '5432')
    database_name = environ['DB_NAME']
    echo = False
    pool_size = 10

    @classmethod
    @lru_cache
    def get_connection_str(cls):
        return f'{cls.dialect}+{cls.driver}://{cls.user}:{cls.password}'\
            f'@{cls.host}:{cls.port}/{cls.database_name}'


class FastapiConfig:
    debug: bool = True
    docs_url: str = '/docs'
    openapi_prefix: str = ''
    openapi_url: str = '/openapi.json'
    redoc_url: str = '/redoc'
    title: str = 'FastAPI example application'
    version: str = '0.0.0'

    @classmethod
    @lru_cache
    def get_fastapi_kwargs(cls) -> dict[str, any]:
        return {
            'debug': cls.debug,
            'docs_url': cls.docs_url,
            'openapi_prefix': cls.openapi_prefix,
            'openapi_url': cls.openapi_url,
            'redoc_url': cls.redoc_url,
            'title': cls.title,
            'version': cls.version,
        }


class AppConfig:
    api_secret_key = environ['API_SECRET_KEY']
    api_key_expire_time = timedelta(days=30)
