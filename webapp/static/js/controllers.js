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

function FileTreeCtrl($scope, $element, Exposure, Hazard){
    $scope.exposure = Exposure;
    $scope.hazard = Hazard;
    
    $($element).fileTree({ script: "http://localhost:5000/filetree" }, function(file) {
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
                //initializeFields(type);
                if (type=='exposure'){
                    $scope.$apply(angular.copy(data, Exposure));
                }else{
                    $scope.$apply(angular.copy(data, Hazard));
                }
            })
            .fail(function(){ alert("Failed to load the style for the impact layer!"); });
        
    });
}

function CalculateCtrl($scope, $element, Exposure, Hazard){
    $scope.exposure = Exposure;
    $scope.hazard = Hazard;
    var br = '<br><br><br><br><br><br><br>';
    var msg = 'Please wait while the system is calculating the results...';
    var progressbar = '<div class="progress progress-striped active">' +
        '<div class="progress-bar"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div>';
    
    $scope.calc = function(){
        $($element).html(br +msg+ progressbar);
        calculate(exposure, exposure_category, exposure_subcategory,
            hazard, hazard_category, hazard_subcategory);
    }
}

//Function that sends a post request containing the filenames of the hazard and exposure layers to the server
function calculate(exposure, exposure_category, exposure_subcategory,
                    hazard, hazard_category, hazard_subcategory){
    $.post("/calculate", 
        {purpose: "calculate", hazard: hazard, hazard_category: hazard_category, hazard_subcategory: hazard_subcategory,
        exposure: exposure, exposure_category: exposure_category, exposure_subcategory: exposure_subcategory})
    .done(function(data){
        var pdf_button = '<button class="btn btn-primary btn-xs pull-left" id="view_pdf"> View PDF </button>';
        $("#results").html(pdf_button + data);
        
        //Create the pdf report
        $.post("/calculate", {purpose: "pdf", html: data});
        
        //Set the onclick listener of the button to show the pdf in a new window
        $("#view_pdf")[0].onclick = function(){
            window.open("/pdf");
        };
        
        //create the impact style of the GeoJson impact layer
        $.getJSON('/impactstyle')
        .done(function(style_info){
            //AJAX call that gets the GeoJson of the impact layer
            $.getJSON('/json', function(geojsonFeature){
                var string = '';
                var myLayer = L.geoJson(geojsonFeature, {
                    style: function(feature){
                        var target_field = style_info.target_field;
                        var target_property = feature.properties[target_field];
                        var color = style_info.style_classes[target_property].colour;
                        return {color: color, weight: 1};
                    }
                }).addTo(map);
                
                $.each(style_info.style_classes, function(k){
                    var label = style_info.style_classes[k].label;
                    var color = style_info.style_classes[k].colour;
                    string += '<i style="background:' +color+ '"></i>' +label+ '<br>';
                });
                map.removeLayer(layers[0]);
                map.removeLayer(layers[1]);
                layers[2] = myLayer;
                div_legend.innerHTML = '<h4>Legend</h4>' + '<i style="background:#E5743D"></i>Hazard<br>' +
                    '<i style="background:#009999"></i>Exposure<br>';
                $(".legend").append(string);
                map.fitBounds(myLayer.getBounds());
            });
        });
    })
    .fail(function(data){
        var msg = 'Please input the necessary data(i.e. exposure, hazard layers).';
        //$("#results").html(br + msg); 
        alert("Request failed!\n Please try again."); 
    });
}

//This function resets the attribute fields of the "type" layer in the layers info sidebar
function initializeFields(type){
    $("#"+type+"_"+"filename").val("");
    $("#"+type+"_"+"name").val("");
    $("#"+type+"_"+"title").val("");
    $("#"+type+"_"+"category").val("");
    $("#"+type+"_"+"subcategory").val("");
}