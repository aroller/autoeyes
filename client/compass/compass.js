//heading is stored so offset can be recorded.
let heading;
// the offset from the bearing to allow for taring
let bearingOffset = 0;

//minimize too many updates
let lastBearingSent = 0;
let lastTimestampSent = 0;

const urlParams = new URLSearchParams(window.location.search);
let host = urlParams.get('host');
const apiUrl = `http://${host}:9090/v1.0`

function initialize() {

    showUpdate(host);
    if (window.DeviceOrientationEvent) {
        getBearingInput().value = '?';
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

let getBearingInput = function () {
    return document.getElementById('bearing');
};

function showUpdate(message){
    document.getElementById('updated').innerText = message;
}
function setBearing(bearing) {
    getBearingInput().value = Math.floor(bearing).toString();
    if (bearing !== lastBearingSent && Date.now() - lastTimestampSent > 100) {
        lastTimestampSent = Date.now();
        lastBearingSent = bearing;
        send('p', bearing);
    }
}

function handleBearingInput(){
    setBearing(getBearingInput().value);
}

/**
 * Tares the bearing to face the current direction so 0 degrees is facing the direction when the button is pressed.
 */
function setCurrentHeadingToFront() {
    bearingOffset = heading;
    showUpdate(`Forward bearing set to heading ${heading}`)
}

function send(actorId, bearinInDegrees) {
    axios.put(`${apiUrl}/actors/${actorId}?bearing=${bearinInDegrees}`).then(data => {

    }, error => {
       showUpdate(error);
    })
}
