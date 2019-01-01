/*
  Shows multiple pedestrians walking in a group and separating.
 */
let carImage;
const scale = 0.5;

const canvasWidth = 400;
const canvasHeight = 400;

const carX = canvasWidth / 2;
const carY = canvasHeight * 2 / 3;

const pedXStart = canvasWidth;
let ped1X = pedXStart;
const ped1Y = 20;
let ped2X = pedXStart;
const ped2Y = 40;
let ped3X = pedXStart;
const ped3Y = 60;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(canvasWidth, canvasHeight);
  carImage = loadCarImage();
}


/**
 * standard processing function called repeatedly
 */
function draw() {
  background(backgroundColor);


  ped1X -= 1;
  ped2X -= 2;
  ped3X -= 3;

  const car = drawCar(carImage, carX, carY, scale);

  if (ped1X > 0) {
    car.addTarget().bearing(ped1X,ped1Y);
  } else {
    ped1X = pedXStart;
    ped2X = pedXStart;
    ped3X = pedXStart;
  }
  if (ped2X > 0) {
    car.addTarget().bearing(ped2X,ped2Y);
  }
  if (ped3X > 0) {
    car.addTarget().bearing(ped3X,ped3Y);
  }
  car.drawLights();

  drawPedestrian(ped1X, ped1Y, "#FF0000");
  drawPedestrian(ped2X, ped2Y, "#FF8800");
  drawPedestrian(ped3X, ped3Y, "#FF00FF");
}


