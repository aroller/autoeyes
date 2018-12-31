/*
  Shows the vehicle watching a bicyclist passing from behind, like in a bikeImage lane.
 */
let carImage;
let bikeImage;

const scale = 0.5;

const canvasWidth = 300;
const canvasHeight = 400;

const carX = canvasWidth / 4;
const carY = canvasHeight / 2;

const bikeX = canvasWidth * 3/4;
const bikeYStart = canvasHeight + 100;
let bikeY = bikeYStart;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(canvasWidth, canvasHeight);
  carImage =  loadCarImage();
  bikeImage = loadBikeImage();
}


/**
 * standard processing function called repeatedly
 */
function draw() {
  background(backgroundColor);

  //when bikeImage is off the page far enough, reset for the repeating loop
  if (bikeY < -200) {
    bikeY = bikeYStart;
  }

  const car = drawCar(carImage,carX, carY, scale);
  //FIXME: the bike should determine if it is on screen
  if (bikeY < canvasHeight && bikeY > -bikeImage.height * scale) {
    car.addTarget().bearing(bikeX,bikeY);
  }
  car.drawLights();
  drawBike(bikeImage, bikeX, bikeY, scale);

  bikeY -= 2;

}


