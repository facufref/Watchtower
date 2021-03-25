const myMap = L.map('mapid').setView([0, 0], 17);
const mapMarkers = []
const mapCircles = []
const source = new EventSource('/topic/watchtower');

// Main Code
addBackgroundMap();
source.addEventListener('message', function(e){
    removeOldLayers();
    let obj = JSON.parse(e.data);
    const towers = obj.towers;
    const threat = obj.threat;

    for (const [ key, value ] of Object.entries(towers)) {
        addMarkers(value, key, 'tower');
    }
    if (threat !== undefined && threat !== null){
        addMarkers(threat, 'Possible Threat', 'threat')
        addCircles(threat)
    }
},false);

//Functions
function addBackgroundMap() {
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiZmFjdWZyZWYiLCJhIjoiY2trZndlNTd6MDk5ODJvazJwazdtM2puMyJ9.tsfgikWw9SWudZzJWt8k3Q'
    }).addTo(myMap);
}

function removeOldLayers() {
    for (let i = 0; i < mapMarkers.length; i++) {
        myMap.removeLayer(mapMarkers[i]);
    }
    for (let i = 0; i < mapCircles.length; i++) {
        myMap.removeLayer(mapCircles[i]);
    }
}

function addMarkers(objectData, objectName, itemType) {
    let marker = L.marker([objectData.lat, objectData.lon], { icon: getMarkerIcon(objectData, objectName, itemType) }).addTo(myMap);
    marker.bindPopup(objectName);
    mapMarkers.push(marker)
}
function getMarkerIcon(objectData, objectKey, itemType) {
    let markerIconUrl;

    if (itemType === 'tower') {
        markerIconUrl = objectData.isThreatDetected === true ? 'static/icons/redMic.png' : 'static/icons/greenMic.png';
    } else if (itemType === 'threat') {
        markerIconUrl = 'static/icons/threat.png'
    }
    return L.icon({
        iconUrl: markerIconUrl,
        iconSize: [40, 40], // size of the icon
    });
}

function addCircles(objectData) {
    let circle = L.circle([objectData.lat, objectData.lon], {
        color: '#e25975',
        fillColor: '#e25975',
        fillOpacity: 0.5,
        radius: objectData.range
    }).addTo(myMap);
    mapCircles.push(circle)
}