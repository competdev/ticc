$(document).ready(function(){

    $.datetimepicker.setLocale('pt-BR');

    $('[widget=time]').mask('00:00');

    $('[widget=date]').datetimepicker({
        timepicker: false,
        format: 'd/m/Y'
    });

    rangeData();

    var trial = {
        'date': $('table tr:nth-child(1) td:nth-child(2)').html(),
        'time': $('table tr:nth-child(2) td:nth-child(2)').html(),
        'location': $('table tr:nth-child(3) td:nth-child(2)').html(),
        'responsible': $('table tr:nth-child(4) td:nth-child(2)').html(),
    }

    // var table = $('.datatables').DataTable({
    //     buttons: [
    //         {
    //             extend: 'print',
    //             autoPrint: false,
    //             className: 'btn-box-tool',
    //             text: '<span class="glyphicon glyphicon-print">',
    //             title: 'Seletiva - Participantes',
    //             message: 
    //                     '<p><strong>Data: </strong>'+trial.date+'</p> \
    //                     <p><strong>Horário: </strong>'+trial.time+'</p> \
    //                     <p><strong>Local: </strong>'+trial.location+'</p> \
    //                     <p><strong>Responsável: </strong>'+trial.responsible+'</p>',
    //             customize: function(win) 
    //             {   
    //                 $(win.document.body)
    //                     .addClass('container');
    //                 $(win.document.body).find('table')
    //                     .addClass('table-bordered'); 
    //                 columns = $('.datatables > tbody').find('> tr:first > td').length;
    //                 for (var i = columns; i > 2; i--) {
    //                     $(win.document.body).find('table tr th:nth-child('+i+'), table tr td:nth-child('+i+')')
    //                         .hide();
    //                 }    
    //             }
    //         },
    //     ],
    //     paging: false,
    //     ordering: true,
    //     info: false,
    //     autoWidth: false,
    //     language: {
    //         emptyTable: 'Nenhum objeto encontrado',
    //         search: 'Buscar'
    //     }
    // });

    // table.on( 'order.dt search.dt', function () {
    //     table.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
    //         cell.innerHTML = i+1;
    //     } );
    // } ).draw()

    // table.buttons().container()
    //     .appendTo(
    //         $('.datatables').closest('.box').find('.box-tools')
    //     );
    // $('.buttons-print').removeClass('btn-default');

});

var rangeData = function(){
    // "dd/mm/yyyy" to "yyyy/mm/dd"
    var dmy2ymd = function(str){
        return str.split('/').reverse().join('/')
    }

    var start = $("#id_start[widget=date]");
    var end = $("#id_end[widget=date]")

    $(start).datetimepicker('destroy');
    $(end).datetimepicker('destroy');

    $(function(){
        $(start).datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            mask: false,
            onShow: function( ct ){
                this.setOptions({
                    maxDate: $(end).val() ? dmy2ymd($(end).val()) : false
                })
            }
        });

        $(end).datetimepicker({
            timepicker: false,
            format: 'd/m/Y',
            mask: false,
            onShow:function( ct ){
                this.setOptions({
                    minDate: $(start).val() ? dmy2ymd($(start).val()) : false
                })
            }
        });
    });
}
