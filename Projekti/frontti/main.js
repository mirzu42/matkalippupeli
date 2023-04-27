'use strict';

const map = L.map('map', {tap: false}).setView([64.18415870306524, 25.801859531170816], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 8,
    minZoom: 3,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    className: 'map-tiles'
}).addTo(map);



const apiUrl = 'http://127.0.0.1:3000/';
const startLoc = '';

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
        document.body.style.backgroundImage='none';
        document.querySelector('article').style.display = 'none'

        element.style.display = 'block'
        setup()
    });

})

document.querySelectorAll('.leaflet-popup-content-wrapper').addEventListener('submit', (evt) => {
    evt.preventDefault()
})

async function getData(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error('Invalid server input!');
  const data = await response.json();
  return data;
}


async function setup(url) {
    try {
        const gameData = await getData(`${apiUrl}airport/fi`);
        gameData.forEach(airport => {
        const marker = L.circleMarker([airport.latitude_deg, airport.longitude_deg], {
            color: 'indigo',
            fillColor: '#1220ec',
            fillOpacity: 0.7,
            radius: 10,
        }).addTo(map).bindTooltip(`${airport.name}`)



        // näyttää nimen ku hiiri on markkerin päällä
       marker.on('click', (e) => {
           marker.bindPopup(airport.name).openPopup()

        })


    });
        let pid = "1"
        const currLocData = await getData(`${apiUrl}loc/${pid}`)
        let currentLoc = currLocData[0].ident

        const airportLine = await getData(`${apiUrl}fly/${currentLoc}`)

        let startLoc = L.latLng(currLocData[0].latitude_deg, currLocData[0].longitude_deg)
        let endLoc = airportLine.map(airport => L.latLng(airport.latitude_deg, airport.longitude_deg));

        console.log(endLoc)
        endLoc.forEach(e => {
            console.log(e)
            const polyline = L.polyline([startLoc, e], {color: 'blue'}).addTo(map);        console.log(polyline)
        })


    } catch (error) {
        console.log(error)
    }
}

//TODO FIKSAA LENTO KNETTÄ VIIVAT esim jos on helsingistä se yhistää currentAirportista 5 viereiseen