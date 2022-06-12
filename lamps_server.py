# start server with `uvicorn <filename>:app 
# --reload for dev to automatically apply code changes
# --port to specify port. Currently client expecting 8888
# --timeout-keep-alive <seconds> to set how long to keep connections open
# --host 0.0.0.0 to allow local connections
# uvicorn lamps_server:app --port 8888 --host 0.0.0.0 --timeout-keep-alive 15

# pi ip: 192.168.86.35 red
# 192.168.86.36 white

from pydantic import BaseModel
import datetime
from fastapi import FastAPI
from copy import copy

app = FastAPI()

class color_post(BaseModel):
    id: str
    color: str

LAMP_ON_DURATION = datetime.timedelta(minutes=60)

LAMP_ON = "lamp_on"
TIME = "delay_time"
COLOR = 'color'
lamp_status = {LAMP_ON: False, TIME: datetime.datetime.now()}

AMANDA_ID = 'amanda'
MARKUS_ID = 'markus'
amanda_lamp = {COLOR: '#d40db3'}
markus_lamp = {COLOR: '#d40db3'}

@app.get("/lamp")
async def get_lamp_on(id: str = None):
    print(id)
    if lamp_status[LAMP_ON] and datetime.datetime.now() > lamp_status[TIME]:
        lamp_status[LAMP_ON] = False

    user_lamp = {}
    if id == AMANDA_ID:
        user_lamp = amanda_lamp
    elif id == MARKUS_ID:
        user_lamp = markus_lamp

    return_status = copy(lamp_status)
    return_status.update(user_lamp)

    return return_status
    # return lamp_status[LAMP_ON]

@app.post("/lamp/on", status_code=201)
async def set_lamp_on():
    lamp_status[TIME] = datetime.datetime.now() + LAMP_ON_DURATION
    lamp_status[LAMP_ON] = True
    return lamp_status[LAMP_ON]

@app.post("/lamp/off", status_code=201)
async def set_lamp_off():
    lamp_status[LAMP_ON] = False
    return lamp_status[LAMP_ON]

@app.post("/lamp/setcolor", status_code=201)
async def set_lamp_color(color_body: color_post):
    id = color_body.id
    color = color_body.color
    if id == MARKUS_ID:
        markus_lamp[COLOR] = color
    elif id == AMANDA_ID:
        amanda_lamp[COLOR] = color

    user_lamp = {}
    if id == AMANDA_ID:
        user_lamp = amanda_lamp
    elif id == MARKUS_ID:
        user_lamp = markus_lamp

    return_status = copy(lamp_status)
    return_status.update(user_lamp)
    return return_status