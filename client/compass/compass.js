


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
            const bearing = 360-alpha;
            document.getElementById('alpha').innerText = Math.floor(alpha).toString();
            document.getElementById('bearing').innerText = Math.floor(bearing).toString();
            document.getElementById('beta').innerText = Math.floor(beta).toString();
            document.getElementById('gamma').innerText = Math.floor(gamma).toString();
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
