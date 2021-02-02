var mymap = L.map('mapid').setView([40.4121, -86.94993], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiZmFjdWZyZWYiLCJhIjoiY2trZndlNTd6MDk5ODJvazJwazdtM2puMyJ9.tsfgikWw9SWudZzJWt8k3Q'
}).addTo(mymap);

mapMarkers = []
circles = []

var source = new EventSource('/topic/watchtower'); //ENTER YOUR TOPICNAME HERE
source.addEventListener('message', function(e){
    obj = JSON.parse(e.data);
    for (var i = 0; i < mapMarkers.length; i++) {
      mymap.removeLayer(mapMarkers[i]);
      mymap.removeLayer(circles[i])
    }
    for (const [ key, value ] of Object.entries(obj)) {
        marker = L.marker([value.lat, value.lon]).addTo(mymap);
        marker.bindPopup(key);
        mapMarkers.push(marker)

        circle = L.circle([value.lat, value.lon], {
            color: value.status === "noise" ? '#82bc6e' : '#e25975',
            fillColor: value.status === "noise" ? '#82bc6e' : '#e25975',
            fillOpacity: 0.5,
            radius: 50 // Pass through parameters
        }).addTo(mymap);
        circles.push(circle)
    }
},false);