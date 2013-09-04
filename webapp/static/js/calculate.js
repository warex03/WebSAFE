var map;

$(function() {
    var hazard;
    var exposure;
    
    $("#tabs").tabs();
    $("#accordion").accordion({
        collapsible: true,
        heightStyle: "content"
    });
    
    $("#hazard").change(function(){
        hazard = $("#hazard").get(0).files[0];
        console.log(hazard);
    });
    
    $("#exposure").change(function(){
        exposure = $("#exposure").get(0).files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            console.log(reader.readAsDataURL(exposure));
            console.log(exposure);
        };
            console.log(reader.readAsDataURL(exposure));
    });
    
    $("#calculate")[0].onclick = function(){
        //Fix the <br> tags with correct css please
        var msg = 'Please wait while the system is calculating the results...'
        var br = '<br><br><br><br><br><br><br><br>';
        var progressbar = '<div class="progress progress-striped active">' +
            '<div class="progress-bar"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div></div>';
        $("#accordion").accordion("option", "active", 1);
        $("#results").html(br +msg+ progressbar)
        calculate(exposure, hazard);
    };
    
    $("#reset")[0].onclick = function(){
        var br = '<br><br><br><br><br><br><br><br>';
        var msg = 'Please input the necessary data(i.e. exposure, hazard layers).';
        $("#results").html(br + msg);
    };
});

function mapInit() {
    map = L.map('map').setView([12.3, 122], 5);
    var gmapsAttrib = '&copy; <a href="http://www.google.com.ph/permissions/geoguidelines.html">Google Maps</a> contributors';
    var gmapsURL = 'http://mt1.google.com/vt/v=w2.106&x={x}&y={y}&z={z}';
    L.tileLayer(gmapsURL, {maxZoom: 18, minZoom: 4, attribution: gmapsAttrib}).addTo(map); 
}

function fileTreeInit(data){
    $("#tabs-1").fileTree({ root: data, script: "/filetree" }, function(file) {
        console.log(file);
        alert(file);
    });
}

function calculate(exposure, hazard){
    $.post("/calculate", {purpose: "calculate"})
    .done(function(data){
        var pdf_button = '<button class="btn btn-primary btn-xs pull-left" id="view_pdf"> View PDF </button>';
        $("#results").html(pdf_button + data);
        /*
        var kmlLayer = new L.KML("/impact", {async: true});
        kmlLayer.on("loaded", function(e) { 
            map.fitBounds(e.target.getBounds());
        });                                   
        map.addLayer(kmlLayer);
        */
        $("#view_pdf")[0].onclick = function(){
            var doc = new jsPDF();
            specialElementHandlers = {
                '#result': function(element, renderer){
                    return true
                }
            }
            
            doc.fromHTML($('#result').get(0), 10, 10, {
                'width': 1000, 'elementHandlers': specialElementHandlers
            });
            
            doc.output('dataurlnewwindow');
        };
        
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
            });
        });
    })
    .fail(function(data){
        alert("POST request to '/calculate' failed!");
    });
}