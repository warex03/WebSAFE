var map;

$(function() {
    var hazard;
    var exposure;
    
    $("#tabs").tabs();
    $("#accordion").accordion({
        collapsible: true,
        heightStyle: "content"
    });
    
    $("#calculate")[0].onclick = function(){
        hazard = $("#hazard_filename").val();
        hazard_name = $("#hazard_name").val();
        hazard_title = $("#hazard_title").val();
        hazard_category = $("#hazard_category").val();
        hazard_subcategory = $("#hazard_subcategory").val();
        
        exposure = $("#exposure_filename").val();
        exposure_name = $("#exposure_name").val();
        exposure_title = $("#exposure_title").val();
        exposure_category = $("#exposure_category").val();
        exposure_subcategory = $("#exposure_subcategory").val();
        
        //Simple client-side validation of required keywords for InaSAFE calculation
        if (isEmpty(hazard) || isEmpty(hazard_name) || isEmpty(hazard_title)
                    || isEmpty(hazard_category) || isEmpty(hazard_subcategory)){    
            alert("Please fill all the hazard fields with correct information!");
        }else if (isEmpty(exposure) || isEmpty(exposure_name) || isEmpty(exposure_title)
                    || isEmpty(exposure_category) || isEmpty(exposure_subcategory)){
            alert("Please fill all the exposure fields with correct information!");
        }else{
            //Fix the <br> tags with correct css please
            var msg = 'Please wait while the system is calculating the results...';
            var br = '<br><br><br><br><br><br><br><br>';
            var progressbar = '<div class="progress progress-striped active">' +
                '<div class="progress-bar"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div>';
            $("#accordion").accordion("option", "active", 1);
            $("#results").html(br +msg+ progressbar);
            calculate(exposure, exposure_category, exposure_subcategory,
                    hazard, hazard_category, hazard_subcategory);
        }
    };
    
    $("#reset")[0].onclick = function(){
        var br = '<br><br><br><br><br><br><br><br>';
        var msg = 'Please input the necessary data(i.e. exposure, hazard layers).';
        initializeFields("exposure");
        initializeFields("hazard");
        $("#results").html(br + msg);
    };
});

function mapInit() {
    map = L.map('map').setView([12.3, 122], 5);
    var gmapsAttrib = '&copy; <a href="http://www.google.com.ph/permissions/geoguidelines.html">Google Maps</a> contributors';
    var gmapsURL = 'http://mt1.google.com/vt/v=w2.106&x={x}&y={y}&z={z}';
    L.tileLayer(gmapsURL, {maxZoom: 18, minZoom: 4, attribution: gmapsAttrib}).addTo(map); 
}

//This function initializes the filetree but also listens to events related to that file tree
function fileTreeInit(data){
    $("#tabs-1").fileTree({ root: data, script: "/filetree" }, function(file) {
        var type;
        //Note: this is a weak way of determining the layer type
        if(file.indexOf("/hazard/") != -1){
            type = "hazard";
        }else if(file.indexOf("/exposure/") != -1){
            type = "exposure";
        }
        
        //gets a GeoJson of the layers of clicked layer item in the file tree and overlays them in the map
        //TODO2: manage layers well. only 1 or 2 layers at a time. max: 3////////////////////////////////////////////////////////////
        //TODO3: updates the 3rd tab for layer ordering//////////////////////////////////////////////////////////////////////////////
        $.getJSON('/layers', {filename: file}, function(geojsonFeature){
            var color = "#009999";
            if(type == "hazard"){
                color = "#E5743D";
            }
            var myLayer = L.geoJson(geojsonFeature, {style: {"color": color}}).addTo(map);
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

//Function that sends a post request containing the filenames of the hazard and exposure layers to the server
function calculate(exposure, exposure_category, exposure_subcategory,
                    hazard, hazard_category, hazard_subcategory){
    $.post("/calculate", 
        {purpose: "calculate", hazard: hazard, hazard_category: hazard_category, hazard_subcategory: hazard_subcategory,
        exposure: exposure, exposure_category: exposure_category, exposure_subcategory: exposure_subcategory})
    .done(function(data){
        var pdf_button = '<button class="btn btn-primary btn-xs pull-left" id="view_pdf"> View PDF </button>';
        $("#results").html(pdf_button + data);
        
        //Create the pdf report asynchronously
        $.post("/calculate", {purpose: "pdf", html: data});
        
        //Set the onclick listener of the button to show the pdf on a new window
        $("#view_pdf")[0].onclick = function(){
            window.open("/pdf");
        };
        
        //create the impact style of the GeoJson impact layer
        $.getJSON('/impactstyle')
        .done(function(style_info){
            //AJAX call that gets the GeoJson of the impact layer
            $.getJSON('/json', function(geojsonFeature){
                var myLayer = L.geoJson(geojsonFeature, {
                    style: function(feature){
                        var target_field = style_info.target_field;
                        var target_property = feature.properties[target_field];
                        return {color: style_info.style_classes[target_property].colour};
                    }
                }).addTo(map);
                map.fitBounds(myLayer.getBounds());
                
                var legend = L.control({position: 'bottomleft'});
                legend.onAdd = function(map){
                        var div = L.DomUtil.create('div', 'info legend'),
                        grades = [0, 10, 20, 50, 100, 200, 500, 1000],
                        labels = [];

                    // loop through our density intervals and generate a label with a colored square for each interval
                    for (var i = 0; i < grades.length; i++) {
                        div.innerHTML +=
                        '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                        grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
                    }

                    return div;
                };
                legend.addTo(map);
            });
        });
    })
    .fail(function(data){ alert("POST request failed!"); });
}

function isEmpty(str) {
    return (!str || 0 === str.length || str == "Not Set");
}