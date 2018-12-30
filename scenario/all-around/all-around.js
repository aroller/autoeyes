let car;

let targetBearing = 0;

const increment = 2*Math.PI/100;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(250,400);

  car = loadImage('../../images/car.png');
}

/**
 * standard processing function called repeatedly
 */
function draw() {
  background(backgroundColor);

  drawCar(125,200, .75, targetBearing += increment );
}


