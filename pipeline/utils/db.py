from dataclasses import dataclass


@dataclass
class DBConnection:
    database: str
    user: str
    pwd: str
    host: str
    port: int


class WarehouseConnection:
    def __init__(self, db_conn: DBConnection):
        self.conn_url = (
            f'postgresql://{db_conn.user}:{db_conn.pwd}@'
            f'{db_conn.host}:{db_conn.port}/{db_conn.database}'
        )

    def connection_string(self):
        return self.conn_url
