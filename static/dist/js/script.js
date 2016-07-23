function initMap() {
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
}

// $(function(){
//     $(".box").hide().each(function(i) {
//         $(this).delay(i*600).fadeIn(600);
//     });
// });

$(document).ready(function(){

    $.datetimepicker.setLocale('pt-BR');

    $('[widget=time]').datetimepicker({
        datepicker: false,
        formatTime: 'H:i',
        mask: true,
        format: 'H:i',
        lang: 'pt-BR'
    });

    $('[widget=date]').datetimepicker({
        timepicker: false,
        formatDate: 'd/m/Y',
        mask: true,
        format: 'd/m/Y',
        defaultDate: new Date(),
        lang: 'pt-BR'
    });

    $('.datatables').DataTable({
        paging: false,
        ordering: true,
        info: false,
        language: {
            emptyTable: 'Nenhum participante encontrado',
            search: 'Buscar'
        },
        order: [
            [2, 'desc'],
            [3, 'asc']
        ]
    });
})

