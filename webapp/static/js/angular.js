var map;
var br = '<br><br><br><br><br><br><br><br>';
var div_legend;
var layers = new Array();

function mapInit() {
    map = L.map('map').setView([12.3, 122], 5);
    var gmapsAttrib = '&copy; <a href="http://www.google.com.ph/permissions/geoguidelines.html">Google Maps</a> contributors';
    var gmapsURL = 'http://mt1.google.com/vt/v=w2.106&x={x}&y={y}&z={z}';
    L.tileLayer(gmapsURL, {maxZoom: 18, minZoom: 5, attribution: gmapsAttrib}).addTo(map);
    var legend = L.control({position: 'bottomleft'});
    legend.onAdd = function(map){
        div_legend = L.DomUtil.create('div', 'info legend');
        div_legend.innerHTML = '<h4>Legend</h4>' + '<i style="background:#E5743D"></i>Hazard<br>' +
            '<i style="background:#009999"></i>Exposure<br>';
        return div_legend;
    };
    legend.addTo(map);
    for(var i=0; i<3; i++){ layers[i] = null; }
}

function isEmpty(str) {
    return (!str || 0 === str.length || str == "Not Set");
}