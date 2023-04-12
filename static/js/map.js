window.onload = init ;
function init(){



    const mapElement = document.getElementById('mapid')
     var map = L.map(mapElement).setView([35, 9.5], 6);
     L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    }).addTo(map);





    // FeatureGroup is to store editable layers
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);
    var drawEditControl = new L.Control.Draw({
        draw: false,
        edit: {
            featureGroup: drawnItems
        }
    });
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems
        }
    });
    map.addControl(drawControl);

    


    map.on('draw:created', function (e) {
        var type = e.layerType;
        layer = e.layer;
            console.log(layer.toGeoJSON());
           
            const   coordinates = layer.toGeoJSON();
            console.log("coord : "+e.layer.toGeoJSON().geometry.coordinates);
            console.log(type);
            if (type === 'polygon'){
                drawnItems.addLayer(layer);
                console.log("coord : "+e.layer.toGeoJSON().geometry.coordinates);
            myjson=drawnItems.toGeoJSON() ;
        console.log(myjson);}
        let coords = [];
        myjson.features.forEach((coordonne) => {
            coords = [...coords, ...coordonne.geometry.coordinates];
        })
            const multiPolygone = { 
                "type": "MultiPolygon",
                "coordinates": [
                    [...coords]
                ]
            }
            console.log(multiPolygone)
        document.getElementById('cord').value=JSON.stringify(multiPolygone);
        
        
        
        
       
       
     })
        
        
        
        
       
       
    //  })

    

    map.on('draw:edited', function (e) {
        layer = e.layers;
        const coordinates = layer._layers[Object.keys(layer._layers)[0]]._latlngs[0];
        let polygon = [];
        coordinates.forEach((element) => {
            polygon.push(`${element.lng} ${element.lat}`);
        });
        polygon.push(`${coordinates[0].lng} ${coordinates[0].lat}`);
        polygonString = 'POLYGON (('+polygon.join(', ')+'))';
        document.getElementById('multiPolygon').value=polygonString;
    });

    map.on('draw:deleted', function () {
        drawControl.addTo(map);
        drawEditControl.remove();
        document.getElementById('multiPolygon').value='';
    });
  



}

