$(function() {
    var hazard;
    var exposure;
    
    $( "#tabs" ).tabs();
    $("#accordion").accordion({
        collapsible: true,
        heightStyle: "content"
    });
    
    $("#hazard").change(function(){
        hazard = $("#hazard").get(0).files[0];
    });
    
    $("#exposure").change(function(){
        exposure = $("#exposure").get(0).files[0];
    });
    
    $("#calculate")[0].onclick = function(){
        calculate(exposure, hazard);
    };
});

function mapInit() {
    var map = L.map('map').setView([12.3, 122], 5);
    var gmapsAttrib = '&copy; <a href="http://www.google.com.ph/permissions/geoguidelines.html">Google Maps</a> contributors';
    var gmapsURL = 'http://mt1.google.com/vt/v=w2.106&x={x}&y={y}&z={z}';
    L.tileLayer(gmapsURL, {maxZoom: 18, minZoom: 4, attribution: gmapsAttrib}).addTo(map);
}

function calculate(exposure, hazard){
    $.post("/calculate")
    .done(function(data){
        $("#results").html(data);
        $("#accordion").accordion("option", "active", 1);
    })
    .fail(function(data){
        alert("POST request to '/calculate' failed!");
    });
}