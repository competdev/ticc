$(document).ready(function() {
    // Inits calendar
    var eventsJson = [];
    events.forEach(function(event) {
        eventsJson.push({
            'start' : event[0], 
            'end': event[1],
            'title': event[2],
            'backgroundColor': event[3],
            'borderColor': event[3],
            'url': event[4]
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
	center: {lat: -19.795875, lng: -43.979034},
        zoom: 13
    });
    var info = new google.maps.InfoWindow({
        content: '<h5>Serviço Social do Comércio <b>SESC</b> - Belo Horizonte</h5>',
        maxWidth: 250
    });
    var marker = new google.maps.Marker({
        position: {lat: -19.795875, lng: -43.979034},
        map: map,
        title: 'sede'
    });
    marker.addListener('click', function() {
        info.open(map, marker);
    });
});
