// the offset from the bearing to allow for taring
let bearingOffset = 0;
let alpha;
let beta;
let gamma;
let bearing;
let heading;

let lastBearingSent = 0;
let lastTimestampSent = 0;
const urlParams = new URLSearchParams(window.location.search);
let host = urlParams.get('host');
const apiUrl = `http://${host}:9090/v1.0`

function initialize() {
    const capableElement = document.getElementById('capable');

    if (window.DeviceOrientationEvent) {
        capableElement.innerText = "True";

        window.addEventListener('deviceorientation', function (event) {
            console.log("orientation triggered");
            document.getElementById('updated').innerText = new Date().toISOString();
            alpha = event.alpha;
            beta = event.beta;
            gamma = event.gamma;
            heading = 360 - alpha;
            bearing = heading - bearingOffset;
            if(bearing < 0){
                bearing = bearing + 360;
            }
            document.getElementById('alpha').innerText = Math.floor(alpha).toString();
            document.getElementById('heading').innerText = Math.floor(heading).toString();
            document.getElementById('bearing').innerText = Math.floor(bearing).toString();
            document.getElementById('beta').innerText = Math.floor(beta).toString();
            document.getElementById('gamma').innerText = Math.floor(gamma).toString();

            if(bearing !== lastBearingSent && Date.now() - lastTimestampSent > 500){
                lastTimestampSent = Date.now();
                lastBearingSent = bearing;
                send('p',bearing);
            }
        }, false);
    } else {
        capableElement.innerHtml = "False";
    }
}

function setCurrentHeadingToFront() {
    bearingOffset = heading;
}

function send(actorId, bearinInDegrees) {
    const lastSend = targetLastSent[actorId];
    if (lastSend === undefined || Math.abs(lastSend - bearinInDegrees) > 1) {
        targetLastSent[actorId] = bearinInDegrees;
        axios.put(`${apiUrl}/actors/${actorId}?bearing=${bearinInDegrees}`).then(data => {
            console.log(data);
        }, error => {
            console.log(e);
        })
    }
}
