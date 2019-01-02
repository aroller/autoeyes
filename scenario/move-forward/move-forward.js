/*
 Shows the vehicle watching a drawPedestrian walk in front, like in a crosswalk.
 */
let carImage;

const canvasWidth = 300;
const pedXOffThePage = canvasWidth + 20;
let pedX = pedXOffThePage;
let car;
let pedTarget;

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
  const carY = 250;
  const pedY = 75;

  drawPedestrian(pedX += 0.25, pedY);

  //the image loads asynchronously so wait until it is ready, otherwise it will produce a bad state
  if(carImage.height > 1){
    if(car){
      car.draw();
    }else{
      car = drawCar(carImage, carX, carY, .50);
      pedTarget = car.addTarget().rightIntent();
    }
    //only show lights when ped is in view
    if (pedX < canvasWidth && pedX > 0) {
      pedTarget.bearing(pedX,pedY);
    }else{
      pedTarget.hidden();
      //reset x with some buffer to repeat loop
      if (pedX > pedXOffThePage) {
        //reset to off the right side of the page
        pedX = -50;
      }
    }
    car.drawLights();

  }


}


