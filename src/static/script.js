function etude_start() {

    var filename = document.getElementById("etude-name");
    var b1 = document.getElementById("B1");
    var b2 = document.getElementById("B2");
    var b3 = document.getElementById("B3");
    var b4 = document.getElementById("B4");
    var b5 = document.getElementById("B5");
    var b6 = document.getElementById("B6");
    
    if (filename.value == "") {
        alert("Veuillez donner un nom à l'étude.");
        return;
    }

    $.ajax({
        type: 'POST',
        url: "http://localhost:5000/etude",
        data: JSON.stringify({
            "params": {
                "filename": filename.value,
                "B1": b1.value,
                "B2": b2.value,
                "B3": b3.value,
                "B4": b4.value,
                "B5": b5.value,
                "B6": b6.value
           }
        }),
        dataType: "json",
        contentType:"application/json",
        complete: function () {
            var etude_running = document.getElementById("etude-running");
            etude_running.style.display = "block";
    
            var etude_params = document.getElementById("etude-params");
            etude_params.style.display = "none";
        }
    });
}

function etude_stop() {
    $.ajax({
        type: 'POST',
        url: "http://localhost:5000/etude",
        data: JSON.stringify({
            "params": {
                "filename": ""
           }
        }),
        dataType: "json",
        contentType:"application/json",
        complete: function () {
            var etude_running = document.getElementById("etude-running");
            etude_running.style.display = "none";
        
            var etude_params = document.getElementById("etude-params");
            etude_params.style.display = "block";
        }
    });
}

function etude_plot() {
    var filename = document.getElementById("etude-name");

    if (filename.value == "") {
        alert("Veuillez donner un nom à l'étude.");
        return;
    }

    $.ajax({
        type: 'POST',
        url: "http://localhost:5000/plot",
        data: JSON.stringify({
            "params": {
                "filename": filename.value
           }
        }),
        dataType: "json",
        contentType:"application/json",
        complete: function (response) {

            if (response.responseText == "erreur") {
                alert("Vérifier le nom de l'étude. Il y a eu une erreur lors du calcul ou de l'exportation des statistiques.")
            }
        }
    });
}

