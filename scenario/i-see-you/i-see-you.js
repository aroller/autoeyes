let carImage;

/**
 * standard processing function called once before draw is called
 */
function setup() {
  createCanvas(300,400);
  background(backgroundColor);
  carImage = loadCarImage();
}


/**
 * standard processing function called repeatedly
 */
function draw() {
  const pedX  = 175;
  const pedY = 75;
  drawPedestrian(pedX,pedY);
  textSize(20);
  text("Pedestrian",130,50);
  text("Light",150,200);
  const car = drawCar(carImage,75,250, .50);
  car.addTarget().bearing(pedX,pedY);
  car.drawLights();

}


