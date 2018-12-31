/*
 Shows the vehicle watching a pedestrian walk in front, like in a crosswalk.
 */
let car;

const pedXOffThePage = -100;
const canvasWidth = 500;
let pedX = pedXOffThePage;
/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(canvasWidth,400);
  car = loadImage('../../images/car.png');
}


/**
 * standard processing function called repeatedly
 */
function draw() {
    background(backgroundColor);

    const carX = canvasWidth/2;
    const carY = 250;
    const pedY = 75;

    pedestrian(pedX-=1,pedY);

    let pedBearing;

    //only show lights when ped is in view
    if(pedX < canvasWidth && pedX > 0) {
      pedBearing = targetBearing(carX,carY,pedX,pedY)
    }



    drawCar(carX,carY, .50,pedBearing);

    //reset x with some buffer to repeat loop
    if(pedX < pedXOffThePage){
      //reset to off the right side of the page
      pedX = canvasWidth + 50;
    }
}


