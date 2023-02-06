
function etude_start() {
    var etude_running = document.getElementById("etude-running");
    etude_running.style.display = "block";

    var etude_params = document.getElementById("etude-params");
    etude_params.style.display = "none";

    
}

function etude_stop() {
    var etude_running = document.getElementById("etude-running");
    etude_running.style.display = "none";

    var etude_params = document.getElementById("etude-params");
    etude_params.style.display = "block";
}

