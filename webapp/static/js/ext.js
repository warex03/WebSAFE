$('#sidebar > li').hover(
    function () { $('a',$(this)).stop().animate({'marginLeft':'-2px'},200); },
    function () { $('a',$(this)).stop().animate({'marginLeft':'-85px'},200); }
);

Ext.application({
    requires: [
        'Ext.container.Viewport',
        'Ext.state.Manager',
        'Ext.state.CookieProvider',
        'Ext.window.MessageBox',
        'GeoExt.panel.Map'
    ],
    
    name: 'NOAH',
    appFolder: '/static/js/app',
    //autoCreateViewport: true,
    
    launch: function() {

        Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider', {
            expires: new Date(new Date().getTime()+(1000*60*60*24*7)) //7 days from now
        }));
        
        var maxExtent = new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34);
		//var layerMaxExtent = new OpenLayers.Bounds(11128623.5489416,-55718.7227285097,16484559.8541582,3072210.74548981);
		var layerMaxExtent = new OpenLayers.Bounds( 11516520.903064, 482870.29798867,  15821300.345956,  2448728.3963715);
		var units = 'm';
		var resolutions = [ 3968.75793751588, 
							2645.83862501058, 
							1322.91931250529, 
							661.459656252646, 
							264.583862501058, 
							132.291931250529, 
							66.1459656252646, 
							26.4583862501058, 
							13.2291931250529, 
							6.61459656252646, 
							2.64583862501058, 
							1.32291931250529, 
							0.661459656252646 ];
		var tileSize = new OpenLayers.Size(256, 256);
		var projection = 'EPSG:900913';
		var tileOrigin = new OpenLayers.LonLat(-20037508.342787,20037508.342787);
		
		var map = new OpenLayers.Map('map', {
			controls: [
                        new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.ScaleLine(),
                        new OpenLayers.Control.MousePosition()
                    ]	,
			maxExtent: maxExtent,
			StartBounds: layerMaxExtent,
			units: units,
			resolutions: resolutions,
			tileSize: tileSize,
			projection: projection,
			restrictedExtent: layerMaxExtent
		});
        
        var wms = new OpenLayers.Layer.ArcGISCache( "Philippine Geoportal Basemap",
			"http://geoportal.gov.ph/ArcGIS/rest/services/Basemap/PGS_Basemap/MapServer", {
			isBaseLayer: true,

			//From layerInfo above                        
			resolutions: resolutions,                        
			tileSize: tileSize,
			tileOrigin: tileOrigin,
			maxExtent: layerMaxExtent, 
			projection: projection,
			displayInLayerSwitcher: false
		},
		{
			//additional options
			transitionEffect: "resize"
		});
        
        map.addLayer(wms);
        
        mappanel = Ext.create('GeoExt.panel.Map', {
            title: 'DOST Project NOAH',
            map: map,
            center: '12.3, 122',
            zoom: 1,
            stateId: 'mappanel',
        });

        Ext.create('Ext.container.Viewport', {
            layout: 'fit',
            items: [
                mappanel
            ]
        });
    }
    
});