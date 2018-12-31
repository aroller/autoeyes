/*
 Shows the vehicle watching a drawPedestrian walk in front, like in a crosswalk.
 */
let carImage;

const pedXOffThePage = -100;
const canvasWidth = 500;
let pedX = pedXOffThePage;

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

  drawPedestrian(pedX -= 1, pedY);


  const car = drawCar(carImage, carX, carY, .50);
  //only show lights when ped is in view
  if (pedX < canvasWidth && pedX > 0) {
    car.addTarget().bearing(pedX,pedY);
  }
  car.drawLights();
  //reset x with some buffer to repeat loop
  if (pedX < pedXOffThePage) {
    //reset to off the right side of the page
    pedX = canvasWidth + 50;
  }
}


