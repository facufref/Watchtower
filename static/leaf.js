var mymap = L.map('mapid').setView([40.4121, -86.94993], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiZmFjdWZyZWYiLCJhIjoiY2trZndlNTd6MDk5ODJvazJwazdtM2puMyJ9.tsfgikWw9SWudZzJWt8k3Q'
}).addTo(mymap);

var wt1 = L.marker([40.41271, -86.9508]).addTo(mymap);
var wt2 = L.marker([40.41301, -86.94991]).addTo(mymap);
var wt3 = L.marker([40.41269, -86.94903]).addTo(mymap);

var wt1_range = L.circle([40.41271, -86.9508], {
    color: 'red',
    fillColor: '#ff0033',
    fillOpacity: 0.5,
    radius: 50
}).addTo(mymap);

var wt2_range = L.circle([40.41301, -86.94991], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 50
}).addTo(mymap);

var wt3_range = L.circle([40.41269, -86.94903], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 50
}).addTo(mymap);

wt1.bindPopup("Watchtower 1");
wt2.bindPopup("Watchtower 2");
wt3.bindPopup("Watchtower 3");