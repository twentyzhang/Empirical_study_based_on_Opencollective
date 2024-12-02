import redis
import timeModel

r = redis.StrictRedis(host='localhost', port=6379, db=0)

start_time = "2024-08-31"
end_time = "2015-01-01"

while start_time >= end_time:
    r.sadd('date_queue', start_time)
    start_time = time.strftime("%Y-%m-%d", time.localtime(time.mktime(time.strptime(start_time, "%Y-%m-%d")) - 86400))