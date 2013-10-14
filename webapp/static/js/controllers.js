var map;
var div_legend;
var layers = new Array();

function MapCtrl($scope) {
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

function fileTreeInit(){
    $("#tabs-1").fileTree({ script: "http://localhost:5000/filetree" }, function(file) {
        /*
        //Note: this is a weak way of determining the layer type
        var type = (file.indexOf("/hazard/") != -1) ? "hazard" : "exposure";

        //gets a GeoJson of the layers of clicked layer item in the file tree and overlays them in the map
        //TODO3: updates the 3rd tab for layer ordering//////////////////////////////////////////////////////////////////////////////
        $.getJSON('/layers', {filename: file}, function(geojsonFeature){
            var color = (type == "hazard") ? "#E5743D" : "#009999";
            var index = (type == "hazard") ? 1 : 0;
            var myLayer = L.geoJson(geojsonFeature, {style: {"color": color, "weight": 1}}).addTo(map);
            if (layers[index] != null){
                map.removeLayer(layers[index]);
                map.removeLayer(layers[2]);
                console.log(layers);
            }
            layers[index] = myLayer;
            map.fitBounds(myLayer.getBounds());
        });

        //update the layer info fields when the user clicks on a file in the file tree
        $.post("/layers", {filename: file, layer_type: type})
            .done(function(data){
                initializeFields(type);
                $("#"+type+"_"+"filename").val(file);
                $.each(data, function(key, val){
                    $("#"+type+"_"+key).val(val);
                });
            })
            .fail(function(){ alert("Failed to load the style for the impact layer!"); });
        */
    });
}