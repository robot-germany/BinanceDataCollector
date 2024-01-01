import psycopg2


class PostgreSQLConnection:
    def __init__(self, params):
        self.params = params
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(**self.params)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
