let car;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(300,500);
  background(backgroundColor);
  car = loadImage('../../images/car.png');
}

function pedestrian(pedX,pedY){

  translate(pedX,pedY);
  fill("#000000");
  ellipse(0,0,20,20);
  strokeWeight(5);
  line(-12, 12,5, 12);
  line(-12,-12,5,-12);
  textSize(20);
  translate(-pedX,-pedY);

}
/**
 * standard processing function called repeatedly
 */
function draw() {
  pedestrian(175,75);
  text("Pedestrian",130,50);
  text("Light",150,200);
  drawCar(75,250, .50, PI/6);



}


