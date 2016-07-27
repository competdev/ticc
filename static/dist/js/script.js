// $(function(){
//     $(".box").hide().each(function(i) {
//         $(this).delay(i*600).fadeIn(600);
//     });
// });

$(document).ready(function(){

    $.datetimepicker.setLocale('pt-BR');

    $('[widget=time]').datetimepicker({
        datepicker: false,
        mask: true,
        format: 'H:i'
    });

    $('[widget=date]').datetimepicker({
        timepicker: false,
        mask: true,
        format: 'd/m/Y'
    });

    rangeData();

    var seletiva = {
        'data': $('table tr:nth-child(1) td:nth-child(2)').html(),
        'horario': $('table tr:nth-child(2) td:nth-child(2)').html(),
        'local': $('table tr:nth-child(3) td:nth-child(2)').html(),
        'responsavel': $('table tr:nth-child(4) td:nth-child(2)').html(),
    }

    var table = $('.datatables').DataTable({
        buttons: [
            {
                extend: 'print',
                autoPrint: false,
                className: 'btn-box-tool',
                text: '<span class="glyphicon glyphicon-print">',
                title: 'Seletiva - Participantes',
                message: 
                        '<p><strong>Data: </strong>'+seletiva.data+'</p> \
                        <p><strong>Horário: </strong>'+seletiva.horario+'</p> \
                        <p><strong>Local: </strong>'+seletiva.local+'</p> \
                        <p><strong>Responsável: </strong>'+seletiva.responsavel+'</p>',
                customize: function(win) 
                {   
                    $(win.document.body)
                        .addClass('container');
                    $(win.document.body).find('table')
                        .addClass('table-bordered'); 
                    columns = $('.datatables > tbody').find('> tr:first > td').length;
                    for (var i = columns; i > 2; i--) {
                        $(win.document.body).find('table tr th:nth-child('+i+'), table tr td:nth-child('+i+')')
                            .hide();
                    }    
                }
            },
        ],
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

    table.buttons().container()
        .appendTo(
            $('.datatables').closest('.box').find('.box-tools')
        );
    $('.buttons-print').removeClass('btn-default');

});

var rangeData = function(){
    // "dd/mm/yyyy" to "yyyy/mm/dd"
    var dmy2ymd = function(str){
        return str.split('/').reverse().join('/')
    }

    $("#id_inicio").datetimepicker('destroy');
    $("#id_termino").datetimepicker('destroy');

    $(function(){
        $("#id_inicio").datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            onShow: function( ct ){
                this.setOptions({
                    maxDate: $("#id_termino").val() ? dmy2ymd($("#id_termino").val()) : false
                })
            }
        });

        $("#id_termino").datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            onShow:function( ct ){
                this.setOptions({
                    minDate: $("#id_inicio").val() ? dmy2ymd($("#id_inicio").val()) : false
                })
            }
        });
    });
}