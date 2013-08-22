$(function() {
    $( "#tabs" ).tabs();
});

$(function() {
    $( "#accordion" ).accordion({
        collapsible: true,
        heightStyle: "content"
    });
    //$('#accordion .ui-accordion-content').show();
});

function mapInit() {
    var map = L.map('map').setView([12.3, 122], 5);
    var gmapsAttrib = '&copy; <a href="http://www.google.com.ph/permissions/geoguidelines.html">Google Maps</a> contributors';
    var gmapsURL = 'http://mt1.google.com/vt/v=w2.106&x={x}&y={y}&z={z}';
    L.tileLayer(gmapsURL, {maxZoom: 18, minZoom: 4, attribution: gmapsAttrib}).addTo(map);
}