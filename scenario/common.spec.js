

function assertEquals(actual,expected,subject){
  assert(actual === expected,`${subject} expected ${expected}, but was ${actual}`)
}

function assert(mustBeTrue,message){
  if(!mustBeTrue){
    throw message;
  }
}

//test bearing calculator
//x grows to the right
//y grows to the bottom
assertEquals(targetBearing(0,0,0,-10),0,"straight ahead");
assertEquals(targetBearing(0,0,10,0) , Math.PI/2,"right bearing");
assertEquals(targetBearing(0,0,0,10), Math.PI,"straight behind");
assertEquals(targetBearing(0,0,-10,0),normalizeRadians(-Math.PI/2),"left bearing");
assertEquals(targetBearing(0,0,10,-10),normalizeRadians(Math.PI/4),"northeast");
assertEquals(targetBearing(0,0,-10,-10),normalizeRadians(-Math.PI/4),"northwest");
assertEquals(targetBearing(0,0,10,10),normalizeRadians(3*Math.PI/4),"southeast");
assertEquals(targetBearing(0,0,-10,10),normalizeRadians(-3*Math.PI/4),"southwest");
