'use strict';

const map = L.map('map', {tap: false}).setView([64.18415870306524, 25.801859531170816], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 8,
    minZoom: 3,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    className: 'map-tiles'
}).addTo(map);

// global
const apiUrl = 'http://127.0.0.1:5000/';
let currentLoc = 'efhk';
const airportMarkers = L.featureGroup().addTo(map);
const polyLine = L.featureGroup().addTo(map)

// piilottaa mapin heti alussa
document.addEventListener('DOMContentLoaded', async (evt) => {
    evt.preventDefault();
    const hideGame = document.querySelectorAll(".gameboard")
    hideGame.forEach((element) => {
        element.style.display = 'none'
        document.querySelector('.kortit').style.display = 'none'; //piilottaa kortit pelin alussa
        document.querySelector('.buttons').style.display = 'none'; //piilottaa napit pelin alussa
    });

})

// piilottaa pelaajan formin kun pelaaja on lisännyt nimen
document.querySelector('#player-form').addEventListener('submit', async(evt) => {
    evt.preventDefault()
    const showGame = document.querySelectorAll(".gameboard")
    showGame.forEach((element) => {
        element.style.display = 'block'
        document.querySelector('#player-input').style.display = 'none'
        document.body.style.backgroundImage='none';
        document.querySelector('article').style.display = 'none'
        document.querySelector('.kortit').style.display = 'flex'; //tuo kortit takaisin näkyviin
        document.querySelector('.buttons').style.display = 'flex'; //tuo napit takaisin näkyviin


        element.style.display = 'block'
    });
    await setup()
    await lentokenttaViivat(currentLoc)


})

const rules = document.getElementsByClassName("button säännöt");
let i;

for(i =0; i < rules.length; i++){
    rules[i].addEventListener("click", function(){
        this.classList.toggle("active");
        const content = this.nextElementSibling;
        if(content.style.display === "block"){
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    })
}




async function lentokenttaViivat(newLoc) {
    console.log("testi " + newLoc)
    const airportLine = await getData(`${apiUrl}flyto?dest=${newLoc}`);
    let currentLoc = await getData(`${apiUrl}/loc/${newLoc}`)
    let startLoc = currentLoc.map(airport => L.latLng(airport.latitude_deg, airport.longitude_deg))
    console.log(startLoc)
    let endLoc = airportLine.map(airport => L.latLng(airport.latitude_deg, airport.longitude_deg));
    console.log(endLoc)

    const newPolyLines = L.featureGroup().addTo(map);

    endLoc.forEach(e => {
        L.polyline([startLoc, e], {color: 'blue'}).addTo(newPolyLines);
    });

}



async function getData(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error('Invalid server input!');
  const data = await response.json();
  return data;
}


async function setup(url) {
    try {
        const gameData = await getData('http://127.0.0.1:3000/airport/fi');
        // lisää markkerit mapille
        gameData.forEach(airport => {
        const marker = L.circleMarker([airport.latitude_deg, airport.longitude_deg], {
            color: 'indigo',
            fillColor: '#1220ec',
            fillOpacity: 0.7,
            radius: 10,
        }).addTo(map).bindTooltip(`${airport.name}`)
            // lisää markereihin formin jotta pelaaja voi vaihtaa kenttää
            airportMarkers.addLayer(marker);
            const popupContent = document.createElement('div');
            const h4 = document.createElement('h4');
            h4.innerHTML = airport.name;
            popupContent.append(h4);
            const goButton = document.createElement('button');
            goButton.classList.add('FlyTo');
            goButton.innerHTML = 'Fly here';
            popupContent.append(goButton);
            marker.bindPopup(popupContent);
            goButton.addEventListener('click',  (e) => {
                const dest = airport.ident;
                setup(`${apiUrl}flyto?dest=${dest}`);
                currentLoc = dest;
                dest.toLowerCase()
                console.log("kissa koira " + dest)
                lentokenttaViivat(dest)
            })
        });


    } catch (error) {
        console.log(error)
    }
}