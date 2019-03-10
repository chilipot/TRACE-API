import redis
pool = redis.ConnectionPool(host='redis', port=6379, db=0)
