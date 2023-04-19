function initMap() {
    const apiKey = 'd2b6d3f37f283ede17cb0f2712517ab8';

    const map = L.map('map').setView([51.505, -0.09], 5);

    const lentokenttaIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/Leaflet/Leaflet/main/dist/images/marker-icon.png',
        iconSize: [25, 40]
    })

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.tileLayer(`https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={apiKey}`, {
        layer: 'temp_new',
        apiKey: apiKey,
        tileSize: 256,
        opacity: 0.5,
        zIndex: 1,
        attribution: '&copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>'
    }).addTo(map);


    async function lentokenttaMarkers() {
        const response = await fetch('http://127.0.0.1:3000/airport/fi')
        const suomiLentokentat = await response.json()
        suomiLentokentat.forEach(airport => {
            L.marker(
                [airport.latitude_deg, airport.longitude_deg],
                {icon: lentokenttaIcon}).addTo(map).bindPopup(`${airport.name}`)
        })
    }
lentokenttaMarkers()


}
document.addEventListener('DOMContentLoaded', initMap);
