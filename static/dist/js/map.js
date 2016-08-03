$(function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -20.172307, lng: -44.910105},
        zoom: 13
    });
    var info = new google.maps.InfoWindow({
        content: '<h5>Centro Federal de Educação Tecnológica de Minas Gerais, <b>Campus V</b> - Divinópolis</h5>',
        maxWidth: 250
    });
    var marker = new google.maps.Marker({
        position: {lat: -20.172307, lng: -44.910105},
        map: map,
        title: 'sede'
    });
    marker.addListener('click', function() {
        info.open(map, marker);
    });
});