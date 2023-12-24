import redis
import json
from datetime import datetime

class TokenBucketAlgo:
    def __init__(self,redis_host='localhost',redis_port=6379,redis_db=0):
        self.redis = redis.StrictRedis(host=redis_host,port=redis_port,db=redis_db)

    def rateLimiter(self,ip,reset_interval,max_req_count):
        key = f"user:{ip}"

        key_exists = self.redis.exists(key)

        if key_exists:
            user_req_data = self.redis.get(key)
            if user_req_data:
                user_req_data = json.loads(user_req_data.decode('utf-8'))
                ip = user_req_data["ip"]
                last_reset_time = user_req_data["last_reset_time"]
                req_left = user_req_data["req_left"]
                current_time = datetime.now()
                current_time_epoch = int(current_time.timestamp())
                if current_time_epoch - last_reset_time >= reset_interval:
                    user_data = {
                        "ip": ip,
                        "last_reset_time":int(datetime.now().timestamp()),
                        "req_left":max_req_count-1
                    }
                    user_json_data = json.dumps(user_data)
                    self.redis.set(key,user_json_data)

                    return (True,max_req_count)
                elif last_reset_time - current_time_epoch < reset_interval and req_left == 0:
                    return (False,req_left)
                elif last_reset_time - current_time_epoch < reset_interval and req_left !=0 and req_left <= max_req_count:
                    user_data = {
                        "ip": ip,
                        "last_reset_time":int(datetime.now().timestamp()),
                        "req_left":req_left-1
                    }
                    user_json_data = json.dumps(user_data)
                    self.redis.set(key,user_json_data)
                    return (True,req_left-1)


                
                    
        else:
            user_data = {
                        "ip": ip,
                        "last_reset_time":int(datetime.now().timestamp()),
                        "req_left":max_req_count-1
                    }
            user_json_data = json.dumps(user_data)
            self.redis.set(key,user_json_data)
            return (True,max_req_count-1)










