//depends on processing.js library
const backgroundColor = "#F2F2F2";


/**
 * Normalizes the radians given to ensure it is within 0 <= x < 2PI
 * @param radians
 * @return {*}
 */
function normalizeRadians(radians) {
  const fullCircle = 2 * Math.PI;
  while (radians >= fullCircle) {
    radians -= fullCircle;
  }
  while (radians < 0) {
    radians += fullCircle;
  }

  return radians;

}



/**
 * Draws the carImage and the light string.
 *
 * @param carImage the image of the carImage to be drawn..preloaded in setup using loadCarImage()
 * @param carX horizontal location for center of the carImage
 * @param carY vertical location for center of the carImage
 * @param scale the multiplier of the size of the image.  1 = full size, < 1 is smaller, > 1 is bigger
 * @param targetBearing the angle, in radians, from the forward center of the carImage
 */
function drawCar(carImage, carX, carY, scale) {


  const carLength = carImage.height * scale;

  //draw the carImage around the center of the given location
  translate(carX, carY);

  const carWidth = carImage.width * scale;

  //draw the carImage first, then the light strip on top
  image(carImage, -carWidth / 2, -carLength / 2, carWidth, carLength);
  translate(-carX, -carY);


  return {

    /**
     * The number of pixels in the light string. More pixels, more granular.
     */
    _pixelCount: 150,

    /**Call addTarget to produce a target */
    _targets: [],

    addTarget: function(){
      const target = {
        _bearing:undefined,
        _lightColor: "#FF0000",
        /**Calculates the bearing to the target from the carImage given the carX,carY*/
        bearing: function (targetX, targetY) {
          this._bearing = targetBearing(carX, carY, targetX, targetY);
        },
        hidden: function(){
          this._bearing = undefined;
        },
        setBearing: function(bearing){
          this._bearing = normalizeRadians(bearing);
        },
      };
      this._targets.push(target);
      return target;
    },
    draw: function(){
      //draw the carImage around the center of the given location
      translate(carX, carY);

      targetBearing = normalizeRadians(targetBearing);
      const carWidth = carImage.width * scale;

      //draw the carImage first, then the light strip on top
      image(carImage, -carWidth / 2, -carLength / 2, carWidth, carLength);
      translate(-carX, -carY);

    },
    /**
     * Draws a light string on top of the carImage highlighting the lights toward the given target.
     */
    drawLights: function () {
      translate(carX, carY);

      const pixelSize = 2;

      //draw each pixel by rotating
      const pixelOffColor = "#000000"
      //light string center is the origin
      const centerPointY = carLength / 8;
      translate(0, centerPointY);
      noStroke();
      const angleBetweenPixels = 2 * Math.PI / this._pixelCount;

      let radius = carLength / 9;
      const angleLitTowardsTarget = Math.PI / 20;

      const pixelX = -pixelSize / 2;
      for (let i = 0; i < this._pixelCount; i++) {
        const bearing = i * angleBetweenPixels;
        let pixelHeight = pixelSize;

        //rectangles start in corner, but center the rectangle for better representation of angle

        let pixelY = -radius - pixelSize / 2;

        const target = anyTargetWithinTolerance(bearing, this._targets, angleLitTowardsTarget);
        //light the pixels towards the target
        if (target) {
          fill(target._lightColor);
          pixelHeight = 70;
          pixelY = pixelY - pixelHeight + pixelSize;
        } else {
          fill(pixelOffColor);
        }
        rect(pixelX, pixelY, pixelSize, pixelHeight);

        //rotate after rectangle since angle = 0 is first
        rotate(angleBetweenPixels);
      }
      //reset the coordinates back to origin allowing future drawing
      translate(-carX, -carY);
    },
  }

}

/**
 * returns true if the target bearing is near the bearing within the tolerance given.
 *
 * @param bearing
 * @param targetBearing
 * @param angleOfTolerance
 * @return {boolean}
 */
function bearingWithinTolerance(bearing, targetBearing, angleOfTolerance) {

  return bearing >= targetBearing - angleOfTolerance && bearing <= targetBearing + angleOfTolerance ||
    //when close to zero, the largest angles may be within tolerance
    bearing >= targetBearing + 2 * PI - angleOfTolerance && bearing <= targetBearing + 2 * PI + angleOfTolerance ||
    //when close to the largest angles, the lowest angles may be within tolerance
    bearing >= targetBearing - 2 * PI - angleOfTolerance && bearing <= targetBearing - 2 * PI + angleOfTolerance;
}

/**
 * Returns one target that is within tolerance, if any.  Which is returned is not determined.
 *
 * @see bearingWithinTolerance
 * @param bearing
 * @param targets
 * @param angleOfTolerance
 * @return {boolean}
 */
function anyTargetWithinTolerance(bearing, targets, angleOfTolerance) {
  let match = undefined;
  targets.forEach(function(target){
    if(bearingWithinTolerance(bearing, target._bearing, angleOfTolerance)){
      match = target;
    }
  });
  return match;
}

/**
 * Draws a drawPedestrian from above at the location given.
 *
 * @param pedX
 * @param pedY
 */
function drawPedestrian(pedX, pedY, color) {

  if (!color) {
    color = "#000000";
  }
  translate(pedX, pedY);
  fill(color);
  ellipse(0, 0, 20, 20);

  translate(-pedX, -pedY);

}

/**
 * Used in the setup function to preload the carImage image for quick drawing in the draw method.
 * @return {*} the carImage image.
 */
function loadCarImage() {
  return loadImage('../../images/car.png');
}

/**
 * Used in the setup function to preload the bikeImage.
 * @return {*} the bikeImage image
 */
function loadBikeImage() {
  return loadImage('../../images/bike.png');
}

/**
 *
 * @param bike the preloaded bikeImage image (use loadBikeImage in setup())
 * @param x the horizontal location of the middle of the bikeImage.
 * @param y the vertical location of the middle of the bikeImage
 * @param scale the size of the bikeImage. 1 = normal, < 1 smaller, > 1 bigger. Natural scale is the same as the carImage
 */
function drawBike(bike, x, y, scale) {
  //draw from the center of the image.  height/4 looked better than /2 for an unknown reason
  image(bike, x - bike.width / 2, y - bike.height / 4, bike.width * scale, bike.height * scale);
}

/** Calculates the angle from the carImage to the target to instruct where the lights should point.
 *
 *  //____ target
 *  //| /
 *  //|/
 *  //carImage
 * @param carX
 * @param carY
 * @param targetX
 * @param targetY
 * @return {number}
 */
function targetBearing(carX, carY, targetX, targetY) {

  //equation for tan2 assumes y grows up, but for us y grows down so no negation necessary
  //https://stackoverflow.com/questions/2676719
  const deltaX = targetX - carX;
  const deltaY = targetY - carY;
  const clockwiseAngleFromXAxis = Math.atan2(deltaY, deltaX);
  const clockwiseAngleFromYAxis = clockwiseAngleFromXAxis + Math.PI / 2;
  return normalizeRadians(clockwiseAngleFromYAxis);
}
