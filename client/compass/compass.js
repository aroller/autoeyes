//heading is stored so offset can be recorded.
let heading;
// the offset from the bearing to allow for taring
let bearingOffset = 0;

//minimize too many updates
let lastBearingSent = 0;
let lastTimestampSent = 0;
let millisecondsBetweenSending = 50;

const urlParams = new URLSearchParams(window.location.search);
let host = urlParams.get('host');

let actorId;
let actorEnabled;
let bearing;
let action;
let direction;
let urgency;

function initialize() {
    if (!host) {
        host = "192.168.50.10"
    }
    actionSelected();
    actorIdSelected();
    actorEnabledSelected();
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
    let now = Date.now();
    if (bearing !== lastBearingSent && now - lastTimestampSent > millisecondsBetweenSending) {
        lastTimestampSent = now;
        lastBearingSent = bearing;
        put();
    }
}

function actionSelected() {
    action = document.querySelector('input[name="action"]:checked').value
    put();
}

function directionSelected() {
    direction = document.querySelector('input[name="direction"]:checked').value
    put();
}

function urgencySelected() {
    urgency = document.querySelector('input[name="urgency"]:checked').value
    put();
}

function actorIdSelected() {
    const selectedActorId = document.querySelector('input[name="actorId"]:checked').value;
    console.log(`${selectedActorId} selected when already selected ${actorId}`);
    if (selectedActorId !== actorId) {
        console.log("sending delete");
        sendDelete();
    }
    actorId = selectedActorId;
    put();
}

function actorEnabledSelected() {
    const enabledValue = document.querySelector('input[name="actorEnabled"]:checked').value;
    const nowEnabled = enabledValue === "on";

    if (!nowEnabled && actorEnabled) {
        sendDelete();
    }

    actorEnabled = nowEnabled;

    if (nowEnabled) {
        put();
    }
}


/**
 * Tares the bearing to face the current direction so 0 degrees is facing the direction when the button is pressed.
 */
function setCurrentHeadingToFront() {
    bearingOffset = heading;
    showUpdate(`Forward bearing set to heading ${heading}`)
}


let getApiUrl = function () {
    return `http://${host}:9090/v1.0`;
};

let baseUrl = function () {
    const apiUrl = getApiUrl();
    const timeSeen = new Date().toISOString();
    return `${apiUrl}/actors/${actorId}?bearing=${bearing}&timeSeen=${timeSeen}`;
};

function put() {
    if(actorEnabled){
        if (actorId) {
            let url = baseUrl();
            if (action) {
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
        } else {
            console.log(`No actor selected.`)
        }
    }else{
        console.log(`Actor is disabled`);
    }


}


function sendDelete() {
    if (actorId) {
        axios.delete(baseUrl()).then(data => {

        }, error => {
            showUpdate(error);
        })
    }
}

function shutDown() {
    let apiUrl1 = getApiUrl();
    axios.put(`${apiUrl1}/systems`).then(data => {
        showUpdate("Shutting down Raspberry PI.");
    }, error => {
        showUpdate(error);
    })
}



