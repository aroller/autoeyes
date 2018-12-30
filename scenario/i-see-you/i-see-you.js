let car;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(300,400);
  background(backgroundColor);
  car = loadImage('../../images/car.png');
}


/**
 * standard processing function called repeatedly
 */
function draw() {
  pedestrian(175,75);
  textSize(20);
  text("Pedestrian",130,50);
  text("Light",150,200);
  drawCar(75,250, .50, PI/6);



}


