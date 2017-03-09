$(document).ready(function() {
    // Inits calendar
    var eventsJson = [];
    events.forEach(function(event) {
        eventsJson.push({
            'start' : event[0], 
            'end': event[1],
            'title': event[2],
            'color': event[3]
        });
    });

    $('#calendar').fullCalendar({
        header: {
            left: 'title',
            center: 'pt-br',
            right:  'today, prev, next'
        },
        locale: 'pt-br',
        height: 500,
        events: eventsJson
    });

    // Inits map
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
