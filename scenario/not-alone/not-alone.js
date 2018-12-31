/*
  Shows the vehicle watching a bicyclist passing from behind, like in a bike lane.
 */
let car;
let bike;

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
  car = loadImage('../../images/car.png');
  loadBike();
}


function loadBike() {
  bike = loadImage('../../images/bike.png');
}

function drawBike(x, y, scale) {
  //draw from the center of the image.  height/4 looked better than /2 for an unknown reason
  image(bike, x - bike.width/2, y-bike.height/4, bike.width * scale, bike.height * scale);
}

/**
 * standard processing function called repeatedly
 */
function draw() {
  background(backgroundColor);

  let bikeBearing;
  //when bike is off the page far enough, reset for the repeating loop
  if (bikeY < -200) {
    bikeY = bikeYStart;
  }

  if (bikeY < canvasHeight && canvasHeight > 0) {
    bikeBearing = targetBearing(carX, carY, bikeX, bikeY);
  }
  drawCar(carX, carY, scale, bikeBearing);
  drawBike(bikeX, bikeY, scale);


  bikeY -= 2;

}


