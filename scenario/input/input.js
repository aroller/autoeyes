/*
 Shows the vehicle watching a drawPedestrian walk in front, like in a crosswalk.
 */
let carImage;

const pedXOffThePage = -100;
const canvasWidth = 300;
let pedX = canvasWidth / 2;
let pedY = 75;

const apiUrlLocal = 'http://localhost:9090/v1.0';
const apiUrlAvEyesLocal = 'http://av-eyes.local:9090/v1.0';

const urlParams = new URLSearchParams(window.location.search);
let host = urlParams.get('host');
host = host? host : 'av-eyes.local';
const apiUrl = `http://${host}:9090/v1.0`
const targetLastSent = {

};

/**
 * standard processing function called once before draw is called
 */
function setup() {
    createCanvas(canvasWidth, 400);
    carImage = loadCarImage();
}


/**
 * standard processing function called repeatedly
 */
function draw() {
    background(backgroundColor);

    const carX = canvasWidth / 2;
    const carY = 200;

    drawPedestrian(pedX, pedY);


    const car = drawCar(carImage, carX, carY, .35);
    //only show lights when ped is in view
    if (pedX < canvasWidth && pedX > 0) {
        const target = car.addTarget().bearing(pedX, pedY);
        const degrees = Math.floor(180 * target.bearing()/Math.PI);
        text( degrees, pedX + 15, pedY + 5)
        send('a',degrees);
    }
    car.drawLights();
    //reset x with some buffer to repeat loop
    if (pedX < pedXOffThePage) {
        //reset to off the right side of the page
        pedX = canvasWidth + 50;
    }
}


function touchStarted() {
    pedX = mouseX;
    pedY = mouseY;
}


function touchMoved() {
    pedX = mouseX;
    pedY = mouseY;
}


function send(actorId,bearinInDegrees){
    const lastSend = targetLastSent[actorId];
    if(lastSend === undefined || Math.abs(lastSend - bearinInDegrees) > 1){
        targetLastSent[actorId] = bearinInDegrees;
        axios.put(`${apiUrl}/actors/${actorId}?bearing=${bearinInDegrees}`).then(data=>{
            console.log(data);
        },error=>{
            console.log(e);
        })
    }
}
