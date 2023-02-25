import express from 'express';

const app = express();

const LAMP_ON_DURATION_MIN = 60;
// initialize the dictionary that holds the lap state
var lamp_status = {lamp_on: false, delay_time: new Date()}

// setup variable needed to store different lamp colors
const AMANDA_ID = 'amanda'
const MARKUS_ID = 'markus'
var amanda_lamp = {color: '#d40db3'}
var markus_lamp = {color: '#d40db3'}

app.listen(3000, () => {
    console.log('The application is listening on port 3000!');
})

app.get("/lamp", (req, res) => {
    if (lamp_status.lamp_on && new Date() > lamp_status.delay_time){
        lamp_status.lamp_on = false
    }

    var user_lamp = {}
    if (req.query.id == AMANDA_ID){
        user_lamp = amanda_lamp
    }
    else if (req.query.id == MARKUS_ID){
        user_lamp = markus_lamp
    }

    // combine the lamp status with the color
    var return_status = {...lamp_status, ...user_lamp};

    res.send(return_status);
})

app.post("/lamp/on", (req, res) => {
    // compute the datetime for when the lamp should turn off
    let now = new Date();
    const MILSEC_PER_MIN = 60 * 1000;
    now.setTime(now.getTime() + LAMP_ON_DURATION_MIN * MILSEC_PER_MIN);
    lamp_status.delay_time = now;
    lamp_status.lamp_on = true;

    res.send(lamp_status.lamp_on)
})

app.post("/lamp/off", (req, res) => {
    lamp_status.lamp_on = false;

    res.send(lamp_status.lamp_on)
})