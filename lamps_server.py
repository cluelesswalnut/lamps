# start server with `uvicorn <filename>:app 
# --reload for dev to automatically apply code changes
# --port to specify port. Currently client expecting 8888
# --timeout-keep-alive <seconds> to set how long to keep connections open
# --host 0.0.0.0 to allow local connections
# uvicorn lamps_server:app --port 8888 --host 0.0.0.0 --timeout-keep-alive 15

# pi ip: 192.168.86.35 red
# 192.168.86.36 white

import datetime
from fastapi import FastAPI

app = FastAPI()

LAMP_ON_DURATION = datetime.timedelta(minutes=60)

LAMP_ON = "lamp_on"
TIME = "delay_time"
lamp_status = {LAMP_ON: False, TIME: datetime.datetime.now()}

@app.get("/lamp")
async def get_lamp_on():
    if lamp_status[LAMP_ON] and datetime.datetime.now() > lamp_status[TIME]:
        lamp_status[LAMP_ON] = False

    return lamp_status[LAMP_ON]

@app.post("/lamp/on", status_code=201)
async def set_lamp_on():
    lamp_status[TIME] = datetime.datetime.now() + LAMP_ON_DURATION
    lamp_status[LAMP_ON] = True
    return lamp_status[LAMP_ON]

@app.post("/lamp/off", status_code=201)
async def set_lamp_off():
    lamp_status[LAMP_ON] = False
    return lamp_status[LAMP_ON]