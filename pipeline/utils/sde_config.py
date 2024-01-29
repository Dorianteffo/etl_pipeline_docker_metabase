import os

from utils.db import DBConnection


def get_warehouse_creds() -> DBConnection:
    return DBConnection(
        user=os.getenv('POSTGRES_USER', ''),
        pwd=os.getenv('POSTGRES_PASSWORD', ''),
        database=os.getenv('POSTGRES_DB', ''),
        host=os.getenv('POSTGRES_HOST', ''),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
    )
