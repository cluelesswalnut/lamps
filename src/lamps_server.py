# start server with `uvicorn <filename>:app
# --reload for dev to automatically apply code changes
# --port to specify port
# --timeout-keep-alive <seconds> to set how long to keep connections open
# --host 0.0.0.0 to allow local connections
# e.g. uvicorn lamps_server:app --port 8888 --host 0.0.0.0 --timeout-keep-alive 15

from pydantic import BaseModel
from copy import copy
import datetime
from fastapi import FastAPI

app = FastAPI()

class ColorPost(BaseModel):
    """
    Holds the fields for a a color post request
    """
    id: str
    color: str

LAMP_ON_DURATION = datetime.timedelta(minutes=60)

# setup field keys
LAMP_ON = "lamp_on"
TIME = "delay_time"
COLOR = 'color'

# initialize the dictionary that holds the lap state
lamp_status = {LAMP_ON: False, TIME: datetime.datetime.now()}

# setup variable needed to store different lamp colors
AMANDA_ID = 'amanda'
MARKUS_ID = 'markus'
amanda_lamp = {COLOR: '#d40db3'}
markus_lamp = {COLOR: '#d40db3'}

@app.get("/lamp")
async def get_lamp_status(id: str = None):
    """
    Check a lamp's status on the server

    @param  id  the id of the lamp to get the status of

    @returns  the status of a lamp including if it is on and the color
    """
    if lamp_status[LAMP_ON] and datetime.datetime.now() > lamp_status[TIME]:
        lamp_status[LAMP_ON] = False

    user_lamp = {}
    if id == AMANDA_ID:
        user_lamp = amanda_lamp
    elif id == MARKUS_ID:
        user_lamp = markus_lamp

    # make a copy of the lamp_status dict to append the user specific
    # color to the copy and return it
    return_status = copy(lamp_status)
    return_status.update(user_lamp)

    return return_status

@app.post("/lamp/on", status_code=201)
async def set_lamp_on():
    """
    Set the lamp's status to on
    """
    lamp_status[TIME] = datetime.datetime.now() + LAMP_ON_DURATION
    lamp_status[LAMP_ON] = True
    return lamp_status[LAMP_ON]

@app.post("/lamp/off", status_code=201)
async def set_lamp_off():
    """
    Set the lamp's status to off
    """
    lamp_status[LAMP_ON] = False
    return lamp_status[LAMP_ON]

@app.post("/lamp/setcolor", status_code=201)
async def set_lamp_color(color_body: ColorPost):
    """
    Set the color of a lamp

    @param  color_body      Contains the color and which user's lamp to set
    """
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