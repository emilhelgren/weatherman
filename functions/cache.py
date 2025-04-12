import redis


class Cache:
    def __init__(self):
        """
        Initialize the redis client.
        """
        self.initiate_cache()


    def initiate_cache(self):
        """
        Initialize the redis client.
        """

        # docker run -p 6379:6379 -it redis/redis-stack:latest
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
            self.redis_client.ping()
            print("Redis client connected successfully.")
        except redis.ConnectionError as e:
            # Handle connection error
            print("Failed to connect to Redis client.")
            print(e)
            self.redis_client = None
        
    def get(self, key):
        """
        Get a value from the cache.
        :param key: The key to get the value for.
        :return: The value for the key.
        """
        if self.redis_client:
            return self.redis_client.get(key)
        else:
            print("Redis client not available.")
            return None
        
    def setex(self, key, timeout, value):
        """
        Set a value in the cache with an expiration time.
        :param key: The key to set the value for.
        :param timeout: The expiration time in seconds.
        :param value: The value to set.
        """
        if self.redis_client:
            self.redis_client.setex(key, timeout, value)
        else:
            print("Redis client not available.")
            return None
        
        
    