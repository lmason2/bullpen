from redis import Redis

class RedisClient():
    connection = None

    def __init__(self) -> None:
        self.connection = Redis()
        self.connection.ping()
        