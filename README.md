# About The Project

Client and server code needed to setup personal friendship lamps.

The friendship lamps use a Raspberry PI connected to LEDs for light and changing colors.
The lamps have a touch sensor used to turn the lamps on. The color can only be changed from a separate mobile app.


# Demo

![Demo](images/lamps.gif)


# Usage

There is a python and a TypeScript version of the server because I wasn't able to make the python server work on the Raspberry PI. This is a WIP.

## TypeScript server

Based on: https://www.linode.com/docs/guides/using-nodejs-typescript-and-express-to-build-a-web-server/

To run in dev environment:
* `npm install`
* `npx ts-node src\lamps_server.ts`

To run on the Raspberry PI:
* `tsc` (this compiles the server into js)
* delete the node_modules dir
* `npm install --omit=dev` to install only the packages required for production. Otherwise the node_modules dir is much larger
* `scp -r node_modules/ pi@<pi-ip>:<location for file>` to transfer the required node_modules files on the the pi
* `scp compiled/lamps_server.js pi@<pi-ip>:<location for file>` to transfer the server js code
* on the pi run `node lamps_server.js`. The node_modules dir needs to be in the same location as the js file.