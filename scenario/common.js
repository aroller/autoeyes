
const backgroundColor = "#F2F2F2";





/**
 * Normalizes the radians given to ensure it is within 0 <= x < 2PI
 * @param radians
 * @return {*}
 */
function normalizeRadians(radians){
  const fullCircle = 2*PI;
  while(radians >= fullCircle){
    radians -= fullCircle;
  }
  while(radians <0){
    radians += fullCircle;
  }

  return radians;

}

/**
 * Draws a light string on top of the car highlighting the lights toward the given target.
 *
 * @param carLength
 * @param targetBearing
 */
let drawLights = function (carLength, targetBearing) {
  const pixelSize = 2;
  const pixelCount = 50;
  //draw each pixel by rotating
  const pixelOffColor = "#000000"
  const lightColor = "#FF0000";
  //light string center is the origin
  const centerPointY = carLength / 8;
  translate(0, centerPointY);
  noStroke();
  const angleBetweenPixels = 2 * PI / pixelCount;
  let radius = carLength / 9;
  fill(lightColor);
  const angleLitTowardsTarget = PI / 16;

  const pixelX = -pixelSize / 2;
  for (let i = 0; i < pixelCount; i++) {
    const bearing = i * angleBetweenPixels;
    let pixelHeight = pixelSize;

    //rectangles start in corner, but center the rectangle for better representation of angle

    let pixelY = -radius - pixelSize / 2;

    //light the pixels towars the target
    if (bearingWithinTolerance(bearing, targetBearing, angleLitTowardsTarget)) {
      fill(lightColor);
      pixelHeight = 70;
      pixelY = pixelY - pixelHeight + pixelSize;
    } else {
      fill(pixelOffColor);
    }
    rect(pixelX, pixelY, pixelSize, pixelHeight);

    //rotate after rectangle since angle = 0 is first
    rotate(angleBetweenPixels);
  }
};

/**
 * Draws the car and the light string.
 *
 * @param x horizontal location for center of the car
 * @param y vertical location for center of the car
 * @param scale the multiplier of the size of the image.  1 = full size, < 1 is smaller, > 1 is bigger
 * @param targetBearing the angle, in radians, from the forward center of the car
 */
function drawCar(x,y,scale, targetBearing) {
  //draw the car around the center of the given location
  translate(x,y);

  targetBearing = normalizeRadians(targetBearing);
  const carWidth = car.width * scale;
  const carLength = car.height * scale;

  //draw the car first, then the light strip on top
  image(car,-carWidth/2,-carLength/2, carWidth , carLength );

  drawLights(carLength, targetBearing);

  //reset the translation to avoid modifying external behavior
  translate(-x,-y);
}

/**
 * returns true if the target bearing is near the bearing within the tolerance given.
 *
 * @param bearing
 * @param targetBearing
 * @param angleOfTolerance
 * @return {boolean}
 */
function bearingWithinTolerance(bearing, targetBearing, angleOfTolerance){

  return bearing >=  targetBearing - angleOfTolerance && bearing <= targetBearing + angleOfTolerance ||
    //when close to zero, the largest angles may be within tolerance
    bearing >= targetBearing + 2*PI - angleOfTolerance && bearing <= targetBearing + 2*PI + angleOfTolerance ||
    //when close to the largest angles, the lowest angles may be within tolerance
    bearing >= targetBearing - 2*PI - angleOfTolerance && bearing <= targetBearing - 2*PI + angleOfTolerance;
}

/**
 * Draws a pedestrian from above at the location given.
 *
 * @param pedX
 * @param pedY
 */
function pedestrian(pedX,pedY){

  translate(pedX,pedY);
  fill("#000000");
  ellipse(0,0,20,20);

  translate(-pedX,-pedY);

}
