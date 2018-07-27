

function report_handler(uuid) {
    var elems = document.getElementsByClassName('report-link');
    var confirmIt = function (e) {
        if (!confirm('¿Está seguro de reportar este enlace?')) {
            e.preventDefault();
        } else {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/posti/report/' + uuid);
            xhr.onload = function (elems) {
                if (xhr.status === 200) {
                    let link = document.getElementsByClassName('report-link')[0];
                    link.parentNode.removeChild(link);
                    let report = document.getElementsByClassName("report");
                    let node = document.createElement("p");
                    let text = document.createTextNode('El reporte se ha realizado exitosamente.');
                    node.appendChild(text);
                    report[0].appendChild(node);
                }
                else {
                    alert('Hubo un error al hacer el reporte.');
                }
            };
            xhr.send();
        }
    };
    for (var i = 0, l = elems.length; i < l; i++) {
        elems[i].addEventListener('click', confirmIt, false);
    }
}

document.addEventListener("DOMContentLoaded", function (event) {
        report_handler(uuid);
});