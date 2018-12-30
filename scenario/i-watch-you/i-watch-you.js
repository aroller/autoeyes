let car;

let pedX = 200;

const canvasWidth = 500;
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

    let targetBearing;

    //only show lights when ped is in view
    if(pedX < canvasWidth && pedX > 0) {
      //____ ped
      //| /
      //|/
      //car
      const adjacent = pedY - carY;
      const opposite = pedX - carX;
      targetBearing = -Math.atan(opposite/adjacent);
    }



    drawCar(carX,carY, .50,targetBearing);

    //reset x with some buffer to repeat loop
    if(pedX < -100){
      //reset to off the right side of the page
      pedX = canvasWidth + 50;
    }
}


