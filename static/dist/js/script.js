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

