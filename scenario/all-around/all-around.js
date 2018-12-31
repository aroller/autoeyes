let carImage;

let fakeTargetBearing = 0;

const increment = 2*Math.PI/100;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(250,400);

  carImage = loadCarImage();
}

/**
 * standard processing function called repeatedly
 */
function draw() {
  background(backgroundColor);

  const car = drawCar(carImage,125,200, .75 );
  car.addTarget().setBearing(fakeTargetBearing += increment);
  car.drawLights();
}


