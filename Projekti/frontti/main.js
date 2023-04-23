'use strict';

const map = L.map('map', {tap: false}).setView([64.18415870306524, 25.801859531170816], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 8,
    minZoom: 3,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    className: 'map-tiles'
}).addTo(map);



const apiUrl = 'http://127.0.0.1:5000/';
const startLoc = '';
const pi = document.querySelector('#player-input')

document.addEventListener('DOMContentLoaded', async (evt) => {
    evt.preventDefault();
    const hideGame = document.querySelectorAll(".gameboard")
    hideGame.forEach((element) => {
        element.style.display = 'none'
    });
})

document.querySelector('#player-form').addEventListener('submit', (evt) => {
    evt.preventDefault()
    const showGame = document.querySelectorAll(".gameboard")
    showGame.forEach((element) => {
        element.style.display = 'block'
        document.querySelector('#player-input').style.display = 'none'
    });

})

async function getData(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error('Invalid server input!');
  const data = await response.json();
  return data;
}


async function lentokenttaMarkers() {
    const gameData = await getData('http://127.0.0.1:3000/airport/fi');


    // looppaa airporttie läpi ja lisää markerit
    gameData.forEach(airport => {
        const marker = L.circleMarker([airport.latitude_deg, airport.longitude_deg], {
            color: 'indigo',
            fillColor: '#1220ec',
            fillOpacity: 0.7,
            radius: 10,
        }).addTo(map)

        // näyttää nimen ku hiiri on markkerin päällä
        marker.on('mouseover', (e) => {
            marker.bindPopup(airport.name).openPopup()
        })
        marker.on('mouseout', (e) => {
            marker.closePopup()
        })

    });

    const airportCoordinates = gameData.map(airport => [airport.latitude_deg, airport.longitude_deg]);
    const polyline = L.polyline(airportCoordinates, {color: 'blue'}).addTo(map);

}


lentokenttaMarkers()
