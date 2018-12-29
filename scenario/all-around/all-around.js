let car;

let targetBearing = 0;

const increment = 2*Math.PI/100;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(200,500);

  car = loadImage('../../images/car.png');
}

/**
 * standard processing function called repeatedly
 */
function draw() {
    drawCar(100,250, .75, targetBearing += increment );
}


