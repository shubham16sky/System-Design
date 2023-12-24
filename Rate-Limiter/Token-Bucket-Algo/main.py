from fastapi import FastAPI,Response,Request
from tokenBucket import TokenBucketAlgo


app = FastAPI()
rateLimiter = TokenBucketAlgo()

#set global Values
RESET_INTERVAL=60
MAX_REQ_COUNT = 3

@app.get("/rateLimiter")
async def limiter(request:Request):
    ip = request.client.host
    result = rateLimiter.rateLimiter(ip=ip,reset_interval=RESET_INTERVAL,max_req_count=MAX_REQ_COUNT)
    

    if result[0]:
        return Response(f"Successfull, you have {result[1]} requests left",status_code=200)
    else:
        return Response(f"Error,you have {result[1]} requests left,try after some time",status_code=429)








        

