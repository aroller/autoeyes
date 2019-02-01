


function initialize(){
    const capableElement = document.getElementById('capable');

    if (window.DeviceOrientationEvent) {
        capableElement.innerText = "True";

        window.addEventListener('deviceorientation', function (event) {
            console.log("orientation triggered");
            document.getElementById('updated').innerText = new Date().toISOString();
            var alpha = event.alpha;
            var beta = event.beta;
            var gamma = event.gamma;
            document.getElementById('alpha').innerText = alpha;
            document.getElementById('beta').innerText = beta;
            document.getElementById('gamma').innerText = gamma;
        }, false);
    } else {
        capableElement.innerHtml = "False";
    }
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
