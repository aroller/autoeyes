//heading is stored so offset can be recorded.
let heading;
// the offset from the bearing to allow for taring
let bearingOffset = 0;

//minimize too many updates
let lastBearingSent = 0;
let lastTimestampSent = 0;

const urlParams = new URLSearchParams(window.location.search);
let host = urlParams.get('host');

let actorId;
let bearing;
let action;
let direction;
let urgency;

function initialize() {
    if(!host){
        host = "10.0.0.179"
    }
    actionSelected();
    actorIdSelected();
    showUpdate(host);
    if (window.DeviceOrientationEvent) {
        window.addEventListener('deviceorientation', function (event) {
            const alpha = event.alpha;
            //store heading globally since it is used for offset
            heading = 360 - alpha;
            let bearing = heading - bearingOffset;
            if (bearing < 0) {
                bearing = bearing + 360;
            }
            setBearing(bearing)

        }, false);
    } else {
        showUpdate("Not Capable");
    }
}


function showUpdate(message) {
    document.getElementById('updated').innerText = message;
}

function setBearing(givenBearing) {
    bearing = Math.floor(givenBearing).toString();
    document.getElementById('bearing').innerText = bearing;
    if (bearing !== lastBearingSent && Date.now() - lastTimestampSent > 50) {
        lastTimestampSent = Date.now();
        lastBearingSent = bearing;
        send();
    }
}

function actionSelected() {
    action = document.querySelector('input[name="action"]:checked').value
    send();
}

function directionSelected() {
    direction = document.querySelector('input[name="direction"]:checked').value
    send();
}

function urgencySelected() {
    urgency = document.querySelector('input[name="urgency"]:checked').value
    send();
}

function actorIdSelected() {
    actorId = document.querySelector('input[name="actorId"]:checked').value
}

/**
 * Tares the bearing to face the current direction so 0 degrees is facing the direction when the button is pressed.
 */
function setCurrentHeadingToFront() {
    bearingOffset = heading;
    showUpdate(`Forward bearing set to heading ${heading}`)
}

function send() {
    const apiUrl = `http://${host}:9090/v1.0`
    let url = `${apiUrl}/actors/${actorId}?bearing=${bearing}`;
    if(action){
        url += `&action=${action}`;
    }
    if (direction && direction !== "none") {
        url += `&direction=${direction}`;
    }
    if (urgency && urgency !== "none") {
        url += `&urgency=${urgency}`;
    }
    axios.put(url).then(data => {

    }, error => {
        showUpdate(error);
    })
}


